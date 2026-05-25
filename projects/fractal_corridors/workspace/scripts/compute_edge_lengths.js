//!/usr/bin/env node
/**
 * Compute Euclidean edge lengths between patches in a synthetic landscape.
 *
 * Usage:
 *   node scripts/compute_edge_lengths.js <budget_file>
 *
 * Example:
 *   node scripts/compute_edge_lengths.js data/synthetic_landscapes/budget_10.json
 *
 * The script reads the JSON, expects a collection of patches each with an
 * identifier and planar coordinates (x, y) expressed in kilometres. It writes a
 * CSV file `output/edge_lengths_<budget>.csv` with three columns:
 *   from_patch,to_patch,length_km
 *
 * The <budget> token is derived from the input filename (e.g., "budget_10").
 * If the filename contains directory separators, only the base name (without
 * extension) is used.
 */

const fs = require('fs');
const path = require('path');

function usage() {
  console.error('Usage: node scripts/compute_edge_lengths.js <budget_file>');
  process.exit(1);
}

if (process.argv.length !== 3) {
  usage();
}

const budgetPath = process.argv[2];
if (!fs.existsSync(budgetPath)) {
  console.error(`File not found: ${budgetPath}`);
  process.exit(1);
}

// Derive a simple budget identifier for the output filename
const budgetBase = path.basename(budgetPath, path.extname(budgetPath));
const outputDir = path.resolve('output');
const outputPath = path.join(outputDir, `edge_lengths_${budgetBase}.csv`);

// Ensure output directory exists
fs.mkdirSync(outputDir, { recursive: true });

let rawData;
try {
  rawData = fs.readFileSync(budgetPath, 'utf-8');
} catch (e) {
  console.error(`Failed to read ${budgetPath}:`, e.message);
  process.exit(1);
}

let json;
try {
  json = JSON.parse(rawData);
} catch (e) {
  console.error('Invalid JSON:', e.message);
  process.exit(1);
}

// Locate patches array – accept either top‑level "patches" property or the root array itself.
let patches = [];
if (Array.isArray(json)) {
  patches = json;
} else if (Array.isArray(json.patches)) {
  patches = json.patches;
} else if (typeof json === 'object' && json.patches && typeof json.patches === 'number') {
  // Synthetic generation: create a regular grid of points based on metadata.
  const num = json.patches;
  const gridSize = json.grid_size_km || 100; // total side length in km
  const spacing = json.average_patch_spacing_km || Math.sqrt(gridSize * gridSize / num);
  const cols = Math.ceil(Math.sqrt(num));
  const rows = Math.ceil(num / cols);
  patches = [];
  let id = 1;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols && id <= num; c++) {
      const x = (c + 0.5) * (gridSize / cols);
      const y = (r + 0.5) * (gridSize / rows);
      patches.push({ id: `p${id}`, x, y });
      id++;
    }
  }
} else {
  console.error('Unable to locate patches array in the JSON file. Expect an array or an object with a "patches" key or a patches count.');
  process.exit(1);
}

// Validate patches have required fields (id, x, y). For synthetic patches, they are guaranteed.
for (const p of patches) {
  if (p.id === undefined || p.x === undefined || p.y === undefined) {
    console.error('Patch missing required fields (id, x, y):', p);
    process.exit(1);
  }
}

function euclidean(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}

let lines = ['from_patch,to_patch,length_km'];
for (let i = 0; i < patches.length; i++) {
  for (let j = i + 1; j < patches.length; j++) {
    const from = patches[i];
    const to = patches[j];
    const dist = euclidean(from, to);
    // Round to three decimal places for readability
    const distStr = dist.toFixed(3);
    lines.push(`${from.id},${to.id},${distStr}`);
  }
}

try {
  fs.writeFileSync(outputPath, lines.join('\n'));
  console.log(`Edge lengths written to ${outputPath}`);
} catch (e) {
  console.error('Failed to write CSV:', e.message);
  process.exit(1);
}
