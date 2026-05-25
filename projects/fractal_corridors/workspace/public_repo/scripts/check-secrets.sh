#!/usr/bin/env bash
set -Eeuo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
env_file="${SECRETS_ENV_FILE:-${repo_root}/.env}"

# shellcheck source=scripts/mask-secrets.sh
source "${script_dir}/mask-secrets.sh"

load_env_file() {
  local file="$1"
  local line key value

  [ -f "${file}" ] || return 0

  while IFS= read -r line || [ -n "${line}" ]; do
    line="${line%$'\r'}"
    case "${line}" in
      ""|\#*) continue ;;
    esac
    line="${line#export }"
    case "${line}" in
      *=*) ;;
      *) continue ;;
    esac
    key="${line%%=*}"
    value="${line#*=}"
    if [[ ! "${key}" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
      continue
    fi
    if [[ "${value}" == \"*\" && "${value}" == *\" ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "${value}" == \'*\' && "${value}" == *\' ]]; then
      value="${value:1:${#value}-2}"
    fi
    export "${key}=${value}"
  done < "${file}"
}

looks_like_placeholder() {
  local value="${1:-}"
  case "${value}" in
    xoxb-your-token|xapp-your-token|your-token|changeme|CHANGE_ME|placeholder|PLACEHOLDER)
      return 0
      ;;
    *your-token*|*placeholder*|*REPLACE*|*replace-me*)
      return 0
      ;;
  esac
  return 1
}

load_env_file "${env_file}"

status=0

require_var() {
  local name="$1"
  local value="${!name:-}"

  if [ -z "${value}" ]; then
    echo "Missing required environment variable: ${name}" >&2
    status=1
    return
  fi

  if looks_like_placeholder "${value}"; then
    echo "Warning: ${name} still looks like a placeholder ($(mask_secret "${value}"))." >&2
    status=1
    return
  fi

  case "${name}" in
    SLACK_BOT_TOKEN|SLACK_APP_TOKEN|OPENAI_API_KEY)
      echo "${name} is set: $(mask_secret "${value}")"
      ;;
    *)
      echo "${name} is set."
      ;;
  esac
}

require_var SLACK_BOT_TOKEN
require_var SLACK_APP_TOKEN
require_var SLACK_DEFAULT_CHANNEL

if [ "${status}" -ne 0 ]; then
  echo "Slack secret validation failed. Copy .env.example to .env, add local tokens, and never commit .env." >&2
  exit "${status}"
fi

echo "Slack secret validation passed."
