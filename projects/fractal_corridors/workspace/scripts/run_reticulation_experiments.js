// ---------------------------------------------------------------
// Reticulation Experiment Driver
// ---------------------------------------------------------------
// This script runs the community model across a realistic
// corridor‑budget spectrum (0.1 % – 30 %) and a set of reticulation
// configurations (0, 1, or 2 extra edges of three types). It records
// all parameters, writes Parquet output, and aggregates results
// in a master JSON log.
//
// Usage:
//   node scripts/run_reticulation_experiments.js
// ---------------------------------------------------------------

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// ----------------------------------------------------------------
// CONFIGURATION
// ----------------------------------------------------------------
const budgets = [
  'budget_0.1.json',
  'budget_5.json',
  'budget_10.json',
  'budget_25.json',
  'budget_30.json',
];

const designs = ['shortest', 'dendritic']; // baseline designs

// Reticulation definition files (stored in data/reticulation/)
const reticDefs = [
  { name: 'none', file: 'retic_0_none.json' },               // pure tree
  { name: 'backbone', file: 'retic_1_backbone.json' },       // 1 extra edge
  { name: 'random', file: 'retic_2_random.json' },          // 2 extra edges
  { name: 'critical', file: 'retic_1_critical.json' },      // 1 high‑mortality edge
];

// Distance‑penalty (γ) values to test – 0 = no penalty, 0.1 = moderate penalty
const gammas = [0, 0.1];

// Output directory for all experiment artefacts
const outDir = path.join(__dirname, '..', 'output', 'reticulation');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

let masterLog = [];

// ----------------------------------------------------------------
// HELPER: run the community model for a single configuration
// ----------------------------------------------------------------
function runExperiment(design, budgetFile, reticFile, gamma, mode=null) {
  // Build command line
  const cmd = [
    'node',
    path.join(__dirname, 'community_model.js'),
    design,
    budgetFile,
    reticFile,
    gamma.toString(),
  ].join(' ');
  console.log(`\n=== Running: ${cmd}`);

  // Execute synchronously; community_model.js writes its own summary JSON
  try {
    execSync(cmd, { stdio: 'inherit' });
  } catch (e) {
    console.error('Model run failed:', e);
    return null;
  }

  // The model writes a summary file named summary_<design>_full.json
  const summaryPath = path.join(__dirname, '..', 'output', `summary_${design}_full.json`);
  if (!fs.existsSync(summaryPath)) {
    console.error('Missing summary file:', summaryPath);
    return null;
  }

  const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));

  // Attach experiment metadata
  const record = {
    design,
    budgetFile,
    reticFile,
    gamma,
    totalEdges: summary.totalEdges,
    totalLengthKm: summary.totalLengthKm,
    finalAbundances: summary.final,
    resilience: summary.resilience,
    parquetPath: summaryPath.replace('summary_', 'community_').replace('.json', '.parquet'),
  };

  // Write a copy of the summary with a unique name for archiving
  const uniqueName = `summary_${design}_${budgetFile.replace('.json','')}_${reticFile.replace('.json','')}_g${gamma}.json`;
  const archivePath = path.join(outDir, uniqueName);
  fs.writeFileSync(archivePath, JSON.stringify(record, null, 2));

  return record;
}

// ----------------------------------------------------------------
// MAIN LOOP
// ----------------------------------------------------------------
for (const design of designs) {
  for (const budgetFile of budgets) {
    for (const retic of reticDefs) {
      for (const gamma of gammas) {
        const result = runExperiment(design, budgetFile, retic.file, gamma);
        if (result) masterLog.push(result);
      }
    }
  }
}

// Write master log
const masterLogPath = path.join(outDir, 'experiment_log.json');
fs.writeFileSync(masterLogPath, JSON.stringify(masterLog, null, 2));
console.log('\nAll experiments completed. Master log written to', masterLogPath);
