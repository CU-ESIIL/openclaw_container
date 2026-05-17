#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

mkdir -p "${HOME}/.openclaw" "${repo_root}/workspace"

if [ "$#" -eq 0 ]; then
  docker compose run --rm --service-ports openclaw-local
else
  docker compose run --rm --service-ports openclaw-local "$@"
fi
