// fetch_gbif_species_traits.js
// This script queries GBIF for species occurring in a specified country (or bounding box).
// It extracts up to 100 unique species and attempts to retrieve dispersal-distance
// information from GBIF literature links. The result is written to
// data/derived/species_traits_gbif.json.

const fs = require('fs');
const path = require('path');

// User‑specified parameters ---------------------------------------------------
// You can edit these constants to change the query region.
// Provide either a country code (ISO 2‑letter) or a GeoJSON polygon string.
const COUNTRY_CODE = "US"; // e.g., "US" for United States. Set to null to use BBOX.
// Bounding box: [minLon, minLat, maxLon, maxLat]
const BBOX = null; // e.g., [-125.0, 24.0, -66.5, 49.5]; // set to null if using country.

// Maximum number of distinct species to retrieve.
const MAX_SPECIES = 100;

// Helper: build GBIF occurrence search URL -----------------------------------
function buildOccurrenceURL(offset = 0, limit = 200) {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
    hasCoordinate: "true",
    // Prefer recent records but not required.
    // Use either country or geometry (bbox) filter.
  });
  if (COUNTRY_CODE) {
    params.append('country', COUNTRY_CODE);
  } else if (BBOX) {
    const [minLon, minLat, maxLon, maxLat] = BBOX;
    const polygon = `POLYGON((${minLon} ${minLat},${maxLon} ${minLat},${maxLon} ${maxLat},${minLon} ${maxLat},${minLon} ${minLat}))`;
    params.append('geometry', polygon);
  }
  return `https://api.gbif.org/v1/occurrence/search?${params.toString()}`;
}

async function fetchJSON(url) {
  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(`Failed to fetch ${url}: ${resp.status}`);
  }
  return await resp.json();
}

async function main() {
  const speciesMap = new Map(); // speciesKey -> {name, traits}
  let offset = 0;
  const batchSize = 200;
  console.log('Fetching occurrences from GBIF...');
  while (speciesMap.size < MAX_SPECIES) {
    const url = buildOccurrenceURL(offset, batchSize);
    const data = await fetchJSON(url);
    if (!data.results || data.results.length === 0) break;
    for (const occ of data.results) {
      if (!occ.speciesKey) continue;
      const key = occ.speciesKey;
      if (!speciesMap.has(key)) {
        const name = occ.species || occ.scientificName || 'unknown';
        speciesMap.set(key, { name, traits: {} });
        if (speciesMap.size >= MAX_SPECIES) break;
      }
    }
    offset += batchSize;
    // Prevent endless loops if GBIF runs out of records.
    if (offset > 5000) break;
  }

  console.log(`Collected ${speciesMap.size} species. Fetching traits...`);

  // For each species, attempt to retrieve dispersal‑distance info.
  for (const [key, rec] of speciesMap) {
    try {
      // 1. Get basic species info (to ensure name correctness).
      const speciesInfo = await fetchJSON(`https://api.gbif.org/v1/species/${key}`);
      rec.name = speciesInfo.canonicalName || rec.name;

      // 2. Get literature references that might contain dispersal data.
      const literature = await fetchJSON(`https://api.gbif.org/v1/species/${key}/literature`);
      // Simple heuristic: look for "dispersal" in titles and extract a numeric value.
      let meanDist = null;
      if (literature.results && literature.results.length > 0) {
        for (const lit of literature.results) {
          const title = lit.title?.toLowerCase() ?? '';
          if (title.includes('dispersal')) {
            // Attempt to find a number followed by "km" or "m".
            const match = lit.title.match(/([0-9]+(?:\.[0-9]+)?)\s*(km|m)/i);
            if (match) {
              const value = parseFloat(match[1]);
              const unit = match[2].toLowerCase();
              meanDist = unit === 'km' ? value * 1000 : value; // store meters
              break;
            }
          }
        }
      }
      // 3. GBIF trait extensions – check the species traits endpoint if present.
      // This endpoint is experimental; we attempt it but ignore failures.
      try {
        const traits = await fetchJSON(`https://api.gbif.org/v1/species/${key}/speciesProfiles`);
        if (traits.results) {
          for (const t of traits.results) {
            if (t.traitName && t.traitName.toLowerCase().includes('dispersal')) {
              // Expect numeric value in t.traitValue
              const val = parseFloat(t.traitValue);
              if (!isNaN(val)) {
                meanDist = val; // assume meters if not specified.
                break;
              }
            }
          }
        }
      } catch (_) { /* ignore */ }

      rec.traits.meanDispersalMeters = meanDist;
      // Kernel shape: use a default exponential kernel if we have a distance.
      rec.traits.kernelShape = meanDist ? 'exponential' : null;
    } catch (e) {
      console.warn(`Failed to process speciesKey ${key}: ${e.message}`);
    }
  }

  // Prepare output array.
  const output = [];
  for (const rec of speciesMap.values()) {
    output.push({
      species: rec.name,
      meanDispersalMeters: rec.traits.meanDispersalMeters ?? null,
      kernelShape: rec.traits.kernelShape ?? null,
    });
  }

  // Ensure output directory exists.
  const outDir = path.join('data', 'derived');
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, 'species_traits_gbif.json');
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2));
  console.log(`Wrote ${output.length} records to ${outPath}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
