#!/usr/bin/env python3
"""Parameter sweep for fractal corridor experiment.

Iterates over a grid of dispersal kernel (σ), road mortality (m), and
stochastic disturbance probability (p). For each combination it runs the
streaming simulation for all network designs (nearest, dendritic, hierarchical,
mst) and records the mean final population.

Outputs a markdown table `analysis/fractal_parameter_sweep.md`.
"""
import itertools, os, subprocess, pathlib, sys
import pandas as pd

# Parameter grids (adjust as needed)
DISPERSAL_KERNELS = [0.05, 0.07, 0.09]
ROAD_MORTALITIES = [0.2, 0.3, 0.4]
DISTURBANCE_PROBS = [0.0, 0.1, 0.2]

city = 'Montreal'
city_dir = pathlib.Path('data/derived') / city
network_files = {
    'nearest': city_dir / 'nearest_web.geojson',
    'dendritic': city_dir / 'dendritic.geojson',
    'hierarchical': city_dir / 'hybrid.geojson',
    'mst': city_dir / 'mst.geojson',
}

results = []
VENV = pathlib.Path('venv')
PYTHON = VENV / 'bin' / 'python3'

for sigma, m, prob in itertools.product(DISPERSAL_KERNELS, ROAD_MORTALITIES, DISTURBANCE_PROBS):
    for label, net_path in network_files.items():
        if not net_path.exists():
            continue
        env = os.environ.copy()
        env['HIERARCHY_TYPE'] = label
        env['DISPERSAL_KERNEL'] = str(sigma)
        env['ROAD_MORTALITY'] = str(m)
        env['DISTURBANCE_PROB'] = str(prob)
        # use a fresh analysis folder per run
        analysis_root = pathlib.Path('analysis') / f'{city}_{label}_sigma{sigma}_m{m}_p{prob}'
        env['ANALYSIS_ROOT'] = str(analysis_root.resolve())
        analysis_root.mkdir(parents=True, exist_ok=True)
        # run the streaming wrapper
        subprocess.run([str(PYTHON), 'scripts/run_simulation_stream.py'], env=env, check=True)
        # read parquet result
        parquet_path = analysis_root / 'simulation_results.parquet'
        if parquet_path.is_file():
            df = pd.read_parquet(parquet_path)
            mean_pop = df['final_population'].mean()
            results.append({
                'design': label,
                'sigma': sigma,
                'mortality': m,
                'disturb_prob': prob,
                'mean_final_population': mean_pop,
            })
        else:
            print(f'WARN: no results for {label} sigma={sigma} m={m} p={prob}', file=sys.stderr)

# Write markdown summary
out_md = pathlib.Path('analysis') / 'fractal_parameter_sweep.md'
with open(out_md, 'w') as f:
    f.write('# Fractal Parameter Sweep Results\n\n')
    f.write('| Design | σ | Mortality | Disturb Prob | Mean Final Population |\n')
    f.write('|--------|---|-----------|--------------|-----------------------|\n')
    for r in results:
        f.write(f"| {r['design']} | {r['sigma']} | {r['mortality']} | {r['disturb_prob']} | {r['mean_final_population']:.2f} |\n")
print('Parameter sweep completed, summary written to', out_md)
