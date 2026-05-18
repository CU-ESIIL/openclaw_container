# Job Launcher Scaffold

This scaffold shows how a trusted ScienceClaw role or human operator can turn an explicit task YAML into a bounded Kubernetes Job manifest.

The launcher is intentionally conservative:

- allowlisted worker images only
- explicit task config file required
- output directory must be under `/data/outputs/jobs`
- no arbitrary shell commands
- no recursive job spawning
- no cluster-admin permissions
- rendered manifests can be reviewed before applying

## Render a Manifest

```bash
python3 runtime/job-launcher/render_job_manifest.py \
  --task examples/spatiotemporal/tasks/example_stac_preview.yaml \
  --job-id example-stac-preview
```

## Submit Deliberately

The submit helper prints the manifest by default. Use `--apply` only after review and with a configured Kubernetes context:

```bash
python3 runtime/job-launcher/submit_k8s_job.py \
  --task examples/spatiotemporal/tasks/example_stac_preview.yaml \
  --job-id example-stac-preview
```

```bash
python3 runtime/job-launcher/submit_k8s_job.py \
  --task examples/spatiotemporal/tasks/example_stac_preview.yaml \
  --job-id example-stac-preview \
  --apply
```

Agents should not call `--apply` unless that permission has been explicitly granted by the human owner for the current project and namespace.
