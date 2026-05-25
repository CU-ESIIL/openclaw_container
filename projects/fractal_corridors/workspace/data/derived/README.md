# Species Traits (GBIF) Data

This directory contains derived data generated from the GBIF API.

## File

- **species_traits_gbif.json** – An array of objects, each with:
  - `species`: Scientific name (string)
  - `meanDispersalMeters`: Estimated mean dispersal distance in meters (number or `null` if not found)
  - `kernelShape`: Suggested dispersal kernel shape (currently `"exponential"` when a distance is available, otherwise `null`)

## Generation script

Run the helper script to (re)create the JSON file:

```bash
node scripts/fetch_gbif_species_traits.js
```

### Parameters (edit the script)
- `COUNTRY_CODE` – ISO‑2 country code (e.g., `"US"`). Set to `null` to use a bounding box.
- `BBOX` – `[minLon, minLat, maxLon, maxLat]` array for a custom region. Set to `null` if using a country.
- `MAX_SPECIES` – Maximum number of distinct species to collect (default 100).

The script queries GBIF occurrence records for the region, collects up to `MAX_SPECIES` unique species, then looks for dispersal‑distance information in literature titles or GBIF trait extensions. Results are written to `species_traits_gbif.json`.

## Usage notes
- The dispersal distance extraction is heuristic; verify values before scientific use.
- If a species lacks published data, `meanDispersalMeters` will be `null`.
- Adjust the region or increase `MAX_SPECIES` as needed for larger projects.
