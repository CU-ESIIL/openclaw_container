# ScienceClaw Workers

Workers are bounded execution containers for reproducible analysis tasks. They are execution boundaries, not autonomous personalities.

The default worker pattern is:

1. A trusted ScienceClaw role drafts or reviews a task YAML.
2. A human or approved launcher runs the task locally or as a Kubernetes Job.
3. The worker streams or samples environmental data where possible.
4. The worker writes reports, figures, tables, logs, `status.json`, and `metadata.json` to `/data/outputs/jobs/<job-id>/`.
5. The output index and workspace UI make artifacts inspectable before any further action.

Workers should not receive arbitrary shell commands. They should receive explicit task configuration files and write to explicit output directories.

## Included Worker

| Worker | Purpose |
| --- | --- |
| `spatiotemporal-worker/` | A conservative STAC/COG/Zarr-oriented analysis worker for stream-first environmental data workflows. |

## Safety Rules

- Use allowlisted worker images.
- Use explicit task config files.
- Use resource limits.
- Do not grant broad filesystem or Kubernetes permissions.
- Do not write secrets to logs or reports.
- Do not let worker jobs recursively launch more jobs.
- Treat outputs as draft artifacts until human review.
