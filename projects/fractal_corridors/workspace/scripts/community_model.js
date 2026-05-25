// Community dynamics model for urban wildlife corridor study
// -----------------------------------------------------------
// This script implements a simple Lotka‑Volterra‑style model for the four
// human‑commensal taxa defined in the literature review:
//   - ground_beetle
//   - mouse
//   - raccoon
//   - bee (optional)
//
// It now supports:
//   1. Budget scaling (via a JSON file in data/synthetic_landscapes/).
//   2. Reticulation definitions (extra edges) that modify encounter factors.
//   3. An optional distance‑penalty term (γ) that reduces growth for longer
//      network paths.
//   4. Automatic CSV → Parquet conversion for efficient downstream analysis.
// -----------------------------------------------------------
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ----- PARAMETERS ------------------------------------------------------
// Intrinsic growth rates (per year) – rough estimates from the literature.
const r = {
  ground_beetle: 0.45, // fast turnover
  mouse: 0.30,
  raccoon: 0.10,
  bee: 0.60,
};

// Carrying capacities – base values (for a full‑budget landscape).
const baseK = {
  ground_beetle: 5000,
  mouse: 2000,
  raccoon: 300,
  bee: 1500,
};

// Time step (years) and total simulation length.
const dt = 0.01; // 0.01 yr ≈ 3.65 days
const tMax = 20; // simulate 20 years

// Load interaction matrix α (per‑capita effect of j on i).
const alphaPath = path.join(__dirname, '..', 'config', 'alpha_matrix.json');
const alpha = JSON.parse(fs.readFileSync(alphaPath, 'utf8'));

// ---------------------------------------------------------------
// Helper: load a budget JSON (if present) and compute scaling factor.
function loadBudgetScale(budgetFile) {
  const defaultPath = path.join(__dirname, '..', 'data', 'synthetic_landscapes', 'budget_10.json');
  const budgetPath = budgetFile ? path.join(__dirname, '..', 'data', 'synthetic_landscapes', budgetFile) : defaultPath;
  if (!fs.existsSync(budgetPath)) return {scale: 1.0, spacing: 1.0};
  const budget = JSON.parse(fs.readFileSync(budgetPath, 'utf8'));
  const percent = budget.budget_percent || 100;
  const spacing = budget.average_patch_spacing_km || 1.0; // km per typical gap between patches
  return {scale: percent / 100.0, spacing: spacing};
}

// Helper: load encounter‑factor CSV for the requested design.
function loadEncounterFactors(design) {
  const csvPath = path.join(__dirname, '..', 'data', `encounter_factors_${design}.csv`);
  if (!fs.existsSync(csvPath)) {
    console.error(`Encounter factor file not found: ${csvPath}`);
    process.exit(1);
  }
  const lines = fs.readFileSync(csvPath, 'utf8').trim().split('\n');
  const factors = {};
  for (let i = 1; i < lines.length; i++) {
    const [iSpecies, jSpecies, factorStr] = lines[i].split(',');
    const key = `${iSpecies}->${jSpecies}`;
    factors[key] = parseFloat(factorStr);
  }
  return { factors, baseEdgeCount: lines.length - 1 };
}

// Helper: load reticulation definition (extra edges) if supplied.
function loadReticulation(reticFile) {
  if (!reticFile) return { extraEdges: [] };
  const reticPath = path.join(__dirname, '..', 'data', 'reticulation', reticFile);
  if (!fs.existsSync(reticPath)) {
    console.warn(`Reticulation file not found: ${reticPath}. Proceeding without extra edges.`);
    return { extraEdges: [] };
  }
  const retic = JSON.parse(fs.readFileSync(reticPath, 'utf8'));
  return retic;
}

// ---------------------------------------------------------------
function simulate(design, budgetFile, reticFile, gamma) {
  const budgetInfo = loadBudgetScale(budgetFile);
  const budgetScale = budgetInfo.scale;
  const spacingKm = budgetInfo.spacing; // average distance between patches (km)
  const K = {
    ground_beetle: baseK.ground_beetle * budgetScale,
    mouse: baseK.mouse * budgetScale,
    raccoon: baseK.raccoon * budgetScale,
    bee: baseK.bee * budgetScale,
  };

  // Load base encounter factors.
  const { factors: baseFactors, baseEdgeCount } = loadEncounterFactors(design);
  // Load reticulation definition.
  const { extraEdges } = loadReticulation(reticFile);

  // Merge extra edges into encounter factor map (override or add).
  let encounter = { ...baseFactors };
  // If mode is 'neutral', set all encounter factors to 1 irrespective of base or extra edges.
  if (mode === 'neutral') {
    // Generate all possible ordered pairs for the four species.
    const species = ['ground_beetle', 'mouse', 'raccoon', 'bee'];
    encounter = {};
    for (const i of species) {
      for (const j of species) {
        if (i !== j) {
          encounter[`${i}->${j}`] = 1.0;
        }
      }
    }
  } else {
    extraEdges.forEach(edge => {
      const key = `${edge.from}->${edge.to}`;
      encounter[key] = edge.factor !== undefined ? edge.factor : 0.8; // default moderate increase
    });
  }

  const totalEdges = baseEdgeCount + extraEdges.length;
  // Approximate total corridor length by multiplying edge count by the average patch spacing (km).
  // This assumes each edge roughly spans the typical distance between habitat patches.
  const totalLengthKm = totalEdges * spacingKm;

  // Initialise populations at 10 % of K (arbitrary starting point).
  const N = {
    ground_beetle: 0.1 * K.ground_beetle,
    mouse: 0.1 * K.mouse,
    raccoon: 0.1 * K.raccoon,
    bee: 0.1 * K.bee,
  };

  const timeSeries = [];
  for (let t = 0; t <= tMax; t += dt) {
    timeSeries.push({
      time: t,
      ground_beetle: N.ground_beetle,
      mouse: N.mouse,
      raccoon: N.raccoon,
      bee: N.bee,
    });

    const dN = {};
    for (const i of Object.keys(N)) {
      // Logistic growth component.
      let d = r[i] * N[i] * (1 - N[i] / K[i]);
      // Interaction sum.
      for (const j of Object.keys(N)) {
        if (i === j) continue;
        const a_ij = (alpha[i] && alpha[i][j]) ? alpha[i][j] : 0;
        const factor = encounter[`${i}->${j}`] ?? 1; // fallback to 1
        d += a_ij * N[i] * N[j] * factor;
      }
      // Optional distance penalty (γ * totalLengthKm) applied uniformly.
      if (gamma) {
        d -= gamma * totalLengthKm * N[i];
      }
      dN[i] = d;
    }
    for (const i of Object.keys(N)) {
      N[i] = Math.max(N[i] + dN[i] * dt, 0);
    }
  }

  // Write CSV and convert to Parquet.
  const outCsv = ['time,ground_beetle,mouse,raccoon,bee'];
  for (const row of timeSeries) {
    outCsv.push(`${row.time.toFixed(3)},${row.ground_beetle.toFixed(2)},${row.mouse.toFixed(2)},${row.raccoon.toFixed(2)},${row.bee.toFixed(2)}`);
  }
  const outCsvPath = path.join(__dirname, '..', 'output', `community_${design}.csv`);
  const outParquetPath = outCsvPath.replace(/\.csv$/i, '.parquet');
  fs.mkdirSync(path.dirname(outCsvPath), { recursive: true });
  fs.writeFileSync(outCsvPath, outCsv.join('\n'));

  try {
    execSync(`python3 - <<'PY'
import pandas as pd, sys
csv_path = r'${outCsvPath}'
parquet_path = r'${outParquetPath}'
df = pd.read_csv(csv_path)
df.to_parquet(parquet_path, index=False)
PY`);
    console.log(`Parquet written to ${outParquetPath}`);
  } catch (e) {
    console.error('Parquet conversion failed:', e);
  }

  // Summarise final abundances and network metrics.
  const summary = {
    design,
    budgetFile,
    reticFile,
    gamma,
    totalEdges,
    totalLengthKm,
    final: {
      ground_beetle: N.ground_beetle,
      mouse: N.mouse,
      raccoon: N.raccoon,
      bee: N.bee,
    },
  };
  const sumPath = path.join(__dirname, '..', 'output', `summary_${design}.json`);
  fs.writeFileSync(sumPath, JSON.stringify(summary, null, 2));
  console.log(`Simulation for '${design}' complete. CSV saved to ${outCsvPath}`);
  return summary;
}

// ---------------------------------------------------------------
function runResilienceTest(baseSummary) {
  // Very simple resilience test: randomly drop 5% of edges by increasing their
  // encounter factor to 0 (effectively removing the interaction). We reuse the
  // same design, budget and reticulation, but modify the encounter CSV on‑the‑fly.
  const { design, budgetFile, reticFile, gamma } = baseSummary;
  // Load base factors to know how many edges exist.
  const { factors: baseFactors, baseEdgeCount } = loadEncounterFactors(design);
  const edgeKeys = Object.keys(baseFactors);
  const dropCount = Math.max(1, Math.floor(edgeKeys.length * 0.05));
  const shuffled = edgeKeys.sort(() => 0.5 - Math.random());
  const toDrop = new Set(shuffled.slice(0, dropCount));

  // Create a temporary modified encounter CSV.
  const tempCsvPath = path.join(__dirname, '..', 'data', `temp_encounter_${design}_${Date.now()}.csv`);
  const lines = ['i,j,factor'];
  edgeKeys.forEach(k => {
    const [iSpec, jSpec] = k.split('->');
    const factor = toDrop.has(k) ? 0 : baseFactors[k];
    lines.push(`${iSpec},${jSpec},${factor}`);
  });
  fs.writeFileSync(tempCsvPath, lines.join('\n'));

  // Run simulation with the temporary CSV (override design by using a special flag).
  // We'll cheat by copying the temp file to the expected location, run, then restore.
  const origPath = path.join(__dirname, '..', 'data', `encounter_factors_${design}.csv`);
  const backupPath = origPath + '.bak';
  fs.copyFileSync(origPath, backupPath);
  fs.copyFileSync(tempCsvPath, origPath);

  const resilienceSummary = simulate(design, budgetFile, reticFile, gamma);

  // Restore original CSV.
  fs.copyFileSync(backupPath, origPath);
  fs.unlinkSync(backupPath);
  fs.unlinkSync(tempCsvPath);

  // Attach resilience difference.
  resilienceSummary.resilienceDrop = {
    droppedEdges: dropCount,
    finalAbundances: resilienceSummary.final,
  };
  return resilienceSummary;
}

// ---------------------------------------------------------------
function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node scripts/community_model.js <design> [budget_file] [reticulation_file] [gamma] [mode]');
    process.exit(1);
  }
  const design = args[0];
  const budgetFile = args[1]; // e.g., "budget_25.json"
  const reticFile = args[2];   // e.g., "retic_1_backbone.json"
  const gamma = args[3] ? parseFloat(args[3]) : 0;
  const mode = args[4] ? args[4].toLowerCase() : null; // "neutral" to set all encounter factors to 1

  const summary = simulate(design, budgetFile, reticFile, gamma, mode);
  // Run a simple resilience test and attach results.
  const resilience = runResilienceTest(summary);
  // Merge resilience info into the original summary file.
  const finalPath = path.join(__dirname, '..', 'output', `summary_${design}_full.json`);
  const combined = { ...summary, resilience };
  fs.writeFileSync(finalPath, JSON.stringify(combined, null, 2));
  console.log('Full summary with resilience written to', finalPath);
}

main();
