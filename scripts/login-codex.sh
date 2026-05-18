#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

mkdir -p "${HOME}/.openclaw" "${repo_root}/workspace"

docker compose run --rm openclaw-local \
  openclaw models auth login --provider openai-codex --set-default "$@"

# Fallback for OpenClaw versions that document onboarding as the Codex OAuth path:
# docker compose run --rm openclaw-local \
#   openclaw onboard --auth-choice openai-codex
