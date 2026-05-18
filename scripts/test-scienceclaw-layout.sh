#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp_root="$(mktemp -d)"
trap 'rm -rf "${tmp_root}"' EXIT

data_root="${tmp_root}/data"

"${repo_root}/scripts/init-data-layout.sh" --data-root "${data_root}" >/tmp/scienceclaw-layout-1.log
"${repo_root}/scripts/init-data-layout.sh" --data-root "${data_root}" >/tmp/scienceclaw-layout-2.log

required_dirs=(
  ".openclaw"
  "workspace"
  "downloads"
  "outputs"
  "outputs/reports"
  "outputs/figures"
  "outputs/tables"
  "outputs/maps"
  "outputs/logs"
  "outputs/jobs"
  "logs"
  "skills/core"
  "skills/experimental"
  "skills/local"
  "agents"
  "memory"
  "notebooks"
  "stac"
  "secrets-example"
)

for dir in "${required_dirs[@]}"; do
  if [ ! -d "${data_root}/${dir}" ]; then
    echo "Missing ScienceClaw data directory: ${data_root}/${dir}" >&2
    exit 1
  fi
  if [ ! -f "${data_root}/${dir}/README.md" ]; then
    echo "Missing README for ScienceClaw data directory: ${data_root}/${dir}" >&2
    exit 1
  fi
done

required_scripts=(
  "scripts/init-data-layout.sh"
  "scripts/setup_env.sh"
  "scripts/check_auth.sh"
  "examples/pdf_to_text.sh"
  "examples/pdf_to_images.sh"
  "examples/markdown_to_html.sh"
  "examples/image_thumbnail_example.sh"
  "examples/playwright_screenshot_example.py"
  "scripts/build_output_index.py"
  "scripts/run_worker_local.sh"
  "scripts/test-spatiotemporal-runtime.sh"
)

for script in "${required_scripts[@]}"; do
  if [ ! -x "${repo_root}/${script}" ]; then
    echo "Expected executable script: ${script}" >&2
    exit 1
  fi
done

python3 -m py_compile "${repo_root}/examples/playwright_screenshot_example.py"

echo "ScienceClaw layout smoke test passed."
