# Data Manifest

This manifest describes the preserved repository snapshot. Gateway 3 has a live project control folder at `/workspace/projects/fractal-corridors` for active work and external mounts.

| Name | Type | Location | Storage mode | License/citation | Sensitivity | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Preserved workspace snapshot | mixed science workspace | `projects/fractal_corridors/workspace` | repository snapshot | review before public reuse | working project material | Contains manuscripts, analysis outputs, scripts, figures, and small data. |
| Compressed Montreal nearest web | GeoJSON gzip | `projects/fractal_corridors/workspace/data/derived/Montreal/nearest_web.geojson.gz` | compressed repository artifact | review before public reuse | working project material | Original GeoJSON was too large for ordinary GitHub use and was compressed. |
| Gateway 3 external shelf | local/remote mount | `/external_storage/local/fractal-corridors` | mount | per dataset | per dataset | Use for future large or credentialed data rather than committing it. |

Before adding new data, document source, access method, format, license, citation requirements, sensitivity, and storage mode.
