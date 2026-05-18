# Kubernetes Scaffold

This directory contains an optional Kubernetes scaffold for ScienceClaw worker jobs. Kubernetes is not required for local use. Docker Compose remains the primary workflow.

The scaffold is designed for future deployment to local `kind` or `minikube`, lab Kubernetes, cloud Kubernetes, ACCESS-CI style execution, or institutional compute environments.

## Design

ScienceClaw treats Kubernetes sub-agents as isolated execution boundaries:

```text
ScienceClaw agent or human reviewer
  -> explicit task YAML
  -> bounded Kubernetes Job
  -> stream-first STAC / COG / Zarr access
  -> persistent /data/outputs artifacts
  -> browser-visible reports, figures, tables, maps, logs
  -> human review
```

The worker is not a personality and does not recursively launch more workers.

## Contents

| Path | Purpose |
| --- | --- |
| `base/` | Namespace and persistent volume claim patterns. |
| `rbac/` | Minimal service account, Role, and RoleBinding examples. |
| `jobs/` | Example bounded analysis Job manifest. |
| `workers/` | Example worker Pod spec. |
| `examples/` | Example task config and secret mounting pattern. |

## Safety Notes

- Do not grant cluster-admin permissions.
- Run ScienceClaw jobs in a dedicated namespace.
- Use resource requests and limits.
- Use `backoffLimit`, `activeDeadlineSeconds`, and explicit output directories.
- Mount only required workspace/output volumes.
- Inject secrets through Kubernetes Secrets or external secret managers, never images or Markdown files.
- Do not mount kubeconfig into the ScienceClaw container unless a human operator explicitly approves that deployment.
- Keep job submission behind bounded templates and allowlisted worker images.

## Example Dry Run

From a configured cluster context:

```bash
kubectl apply --dry-run=server -k deploy/kubernetes/base
kubectl apply --dry-run=server -f deploy/kubernetes/jobs/example-spatiotemporal-job.yaml
```

For local development without a cluster, use:

```bash
./scripts/run_worker_local.sh examples/spatiotemporal/tasks/example_stac_preview.yaml --offline
```
