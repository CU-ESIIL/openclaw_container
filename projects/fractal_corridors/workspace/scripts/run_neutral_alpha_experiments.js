// ---------------------------------------------------------------
// Neutral‑α experiment driver
// ---------------------------------------------------------------
// Runs the community model for all budget levels (0.1% – 30%) and both
// designs (shortest, dendritic) with encounter factors forced to 1.
// The script records final abundances, a simple Shannon diversity
// index, total corridor length, and writes a consolidated JSON log.
// ---------------------------------------------------------------

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const budgets = [
  'budget_0.1.json',
  'budget_5.json',
  'budget_10.json',
  'budget_25.json',
  'budget_30.json',
];
const designs = ['shortest', 'dendritic'];
const reticFile = 'retic_0_none.json'; // reticulation irrelevant when mode=neutral
const gamma = 0; // no distance penalty for baseline neutral runs

const outDir = path.join(__dirname, '..', 'output', 'reticulation');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

function shannon(abundances) {
  const total = Object.values(abundances).reduce((a,b)=>a+b,0);
  if (total===0) return 0;
  let h = 0;
  for (const v of Object.values(abundances)) {
    if (v>0) {
      const p = v/total;
      h -= p*Math.log(p);
    }
  }
  return h;
}

let master = [];

for (const design of designs) {
  for (const budgetFile of budgets) {
    const cmd = [
      'node',
      path.join(__dirname, 'community_model.js'),
      design,
      budgetFile,
      reticFile,
      gamma.toString(),
      'neutral' // mode argument forces encounter factors=1
    ].join(' ');
    console.log(`\n=== Running neutral‑α: ${cmd}`);
    try {
      execSync(cmd, { stdio: 'inherit' });
    } catch (e) {
      console.error('Run failed:', e);
      continue;
    }
    // Load the JSON summary produced by community_model.js
    const summaryPath = path.join(__dirname, '..', 'output', 'summary_' + design + '_full.json');
    if (!fs.existsSync(summaryPath)) {
      console.error('Missing summary file for', design, budgetFile);
      continue;
    }
    const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
    const diversity = shannon(summary.final);
    const record = {
      design,
      budgetFile,
      totalEdges: summary.totalEdges,
      totalLengthKm: summary.totalLengthKm,
      finalAbundances: summary.final,
      shannonDiversity: diversity,
    };
    master.push(record);
  }
}

const logPath = path.join(outDir, 'neutral_alpha_log.json');
fs.writeFileSync(logPath, JSON.stringify(master, null, 2));
console.log('\nNeutral‑α experiment complete. Log written to', logPath);
