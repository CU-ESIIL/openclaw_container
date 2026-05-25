// simulate_corridor_population_dynamics.js
// Updated to output results directly to Parquet using a Python bridge (pyarrow)
// and perform a brief sensitivity analysis on dispersal kernel and disturbance intensity.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const ANALYSIS_DIR = path.join(ROOT, 'analysis', 'urban_wildlife_corridors');
const OUTPUT_PARQUET = path.join(ANALYSIS_DIR, 'simulation_results.parquet');

// Ensure output directory exists
fs.mkdirSync(ANALYSIS_DIR, { recursive: true });

// ---------- Core Simulation (placeholder) ----------
// In a real project this would run the corridor population dynamics model.
// Here we generate a simple synthetic dataset for demonstration.
function runSimulation(params) {
  const rows = [];
  const { replicates, steps, dispersalKernel, disturbanceIntensity } = params;
  for (let rep = 0; rep < replicates; rep++) {
    let pop = 100; // start population
    for (let step = 0; step < steps; step++) {
      // simple dynamics: growth with stochastic component, modulated by kernel & disturbance
      const growth = pop * (0.02 + Math.random() * 0.01);
      const loss = pop * (dispersalKernel * 0.05 + disturbanceIntensity * 0.1);
      pop = Math.max(pop + growth - loss, 0);
    }
    rows.push({ replicate: rep + 1, final_population: pop, dispersalKernel, disturbanceIntensity });
  }
  return rows;
}

// Default parameters
const DEFAULT_PARAMS = {
  replicates: 30,
  steps: 500,
  dispersalKernel: 0.07, // baseline kernel value
  disturbanceIntensity: 0.1, // baseline disturbance
};

// Run base simulation
const baseResults = runSimulation(DEFAULT_PARAMS);

// ---------- Sensitivity Analysis ----------
// Vary dispersal kernel and disturbance intensity across a small grid.
const kernelVals = [0.05, 0.07, 0.09];
const disturbanceVals = [0.05, 0.1, 0.2];
const sensitivityResults = [];
for (const k of kernelVals) {
  for (const d of disturbanceVals) {
    const params = { ...DEFAULT_PARAMS, dispersalKernel: k, disturbanceIntensity: d };
    const res = runSimulation(params);
    // summarise mean final population
    const meanPop = res.reduce((a, r) => a + r.final_population, 0) / res.length;
    sensitivityResults.push({ dispersalKernel: k, disturbanceIntensity: d, mean_final_population: meanPop.toFixed(2) });
  }
}

// ---------- Helper: write JSON data to a temporary file ----------
function writeTempJson(data) {
  const tmpPath = path.join(ANALYSIS_DIR, 'temp_simulation.json');
  fs.writeFileSync(tmpPath, JSON.stringify(data, null, 2));
  return tmpPath;
}

// Write base results to Parquet via Python bridge
function writeParquetViaPython(jsonPath, parquetPath) {
  // Inline Python script that reads JSON and writes Parquet using pyarrow
  const pythonScript = `
import json, sys, pyarrow as pa, pyarrow.parquet as pq
json_path = sys.argv[1]
parquet_path = sys.argv[2]
with open(json_path, 'r') as f:
    data = json.load(f)
# Convert list of dicts to Arrow table
table = pa.Table.from_pydict({k: [row[k] for row in data] for k in data[0].keys()})
pq.write_table(table, parquet_path)
`;
  // Write the script to a temporary file
  const scriptPath = path.join(ANALYSIS_DIR, 'write_parquet.py');
  fs.writeFileSync(scriptPath, pythonScript);
  // Execute the script
  execSync(`python3 ${scriptPath} ${jsonPath} ${parquetPath}`);
  // Cleanup temporary files
  fs.unlinkSync(scriptPath);
  fs.unlinkSync(jsonPath);
}

const baseJsonPath = writeTempJson(baseResults);
writeParquetViaPython(baseJsonPath, OUTPUT_PARQUET);

// ---------- Export Sensitivity Table (Markdown) ----------
function generateSensitivityMarkdown(table) {
  let md = '| Dispersal Kernel | Disturbance Intensity | Mean Final Population |\n';
  md += '|------------------|-----------------------|-----------------------|\n';
  for (const row of table) {
    md += `| ${row.dispersalKernel} | ${row.disturbanceIntensity} | ${row.mean_final_population} |\n`;
  }
  return md;
}

const sensitivityMarkdown = generateSensitivityMarkdown(sensitivityResults);

// Write the markdown to a supplemental file for later inclusion
fs.writeFileSync(path.join(ANALYSIS_DIR, 'sensitivity_table.md'), sensitivityMarkdown);

console.log('Simulation complete. Parquet written to', OUTPUT_PARQUET);
console.log('Sensitivity analysis markdown written to', path.join(ANALYSIS_DIR, 'sensitivity_table.md'));
