# Makefile for Urban Wildlife Corridor Project

# Directories
DATA_DIR = data
RAW_DIR = $(DATA_DIR)/raw
DERIVED_DIR = $(DATA_DIR)/derived
OUTPUT_DIR = output
SCRIPT_DIR = scripts

# Python environment (assumes required packages are installed)
PYTHON = python3

# Targets

# 1a. Fetch GBIF species traits (new)
fetch_gbif_traits:
	node $(SCRIPT_DIR)/fetch_gbif_species_traits.js

# 0. Download NDVI from Sentinel‑2 (new)
download_ndvi:
	$(PYTHON) $(SCRIPT_DIR)/download_ndvi_sentinel2.py --tile T31TFJ --date 2023-06-15 --output $(DERIVED_DIR)/ndvi.tif

.PHONY: all generate_landscape generate_cost_matrix generate_ensembles run_simulation

all: generate_landscape generate_cost_matrix generate_ensembles run_simulation

# 1. Generate heterogeneous landscape (80-120 patches) -> data/derived/patches.geojson
generate_landscape:
	$(PYTHON) $(SCRIPT_DIR)/generate_landscape.py

# 2. Build effective‑cost matrix (Euclidean + road density + species penalties) -> data/derived/cost_matrix.npy
generate_cost_matrix:
	$(PYTHON) $(SCRIPT_DIR)/generate_cost_matrix.py

# 3. Generate stochastic network ensembles preserving total cost or degree distribution
#    Output: data/derived/networks/*.json
generate_ensembles:
	$(PYTHON) $(SCRIPT_DIR)/generate_ensembles.py

# 4. Run the metacommunity simulation using the JavaScript scaffold.
#    This will read the cost matrix and patch file.
run_simulation:
	node $(SCRIPT_DIR)/simulate_corridor_population_dynamics.js

# Convenience shortcut to run the full pipeline
pipeline: all
