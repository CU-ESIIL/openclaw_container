#!/usr/bin/env bash
set -Eeuo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <instance-name> [gateway-port] [workspace-ui-port] [cms-port]" >&2
  echo "Example: $0 project-two 18790 8889 8091" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

instance_name="$1"
gateway_port="${2:-18790}"
workspace_ui_port="${3:-8889}"
cms_port="${4:-8091}"
instance_root="${repo_root}/instances/${instance_name}"

mkdir -p \
  "${instance_root}/data" \
  "${instance_root}/workspace" \
  "${instance_root}/external_storage" \
  "${instance_root}/openclaw"

if [ "${ENABLE_INSTANCE_SLACK:-0}" = "1" ]; then
  "${repo_root}/scripts/check-secrets.sh"
else
  export SLACK_BOT_TOKEN=""
  export SLACK_APP_TOKEN=""
  export SLACK_DEFAULT_CHANNEL=""
fi

project_name="scienceclaw-${instance_name}"

env_args=(
  --project-name "${project_name}"
)

export SCIENCECLAW_CONTAINER_NAME="openclaw-${instance_name}"
export DATA_DIR="${instance_root}/data"
export WORKSPACE_DIR="${instance_root}/workspace"
export EXTERNAL_STORAGE_DIR="${instance_root}/external_storage"
export OPENCLAW_STATE_DIR="${OPENCLAW_STATE_DIR:-${instance_root}/openclaw}"
export OPENCLAW_GATEWAY_PORT="${gateway_port}"
export OPENCLAW_CONTROL_ORIGINS="http://127.0.0.1:${gateway_port},http://localhost:${gateway_port}"
export OPENCLAW_DEFAULT_MODEL="${OPENCLAW_DEFAULT_MODEL:-verde/js2/gpt-oss-120b}"
export OPENCLAW_MODEL="${OPENCLAW_MODEL:-verde/js2/gpt-oss-120b}"
export WORKSPACE_UI_PORT="${workspace_ui_port}"
workspace_ui_token="${WORKSPACE_UI_TOKEN:-scienceclaw}"
export SCIENCECLAW_CMS_PORT="${cms_port}"
export OPENCLAW_START_PI_LIAISON=0
export OPENCLAW_CONFIGURE_SLACK="${OPENCLAW_CONFIGURE_SLACK:-0}"

config_path="${OPENCLAW_STATE_DIR}/openclaw.json"
if [ -f "${config_path}" ]; then
  node - "${config_path}" "${gateway_port}" "${OPENCLAW_CONTROL_ORIGINS}" <<'NODE'
const fs = require("fs");
const [configPath, port, originsRaw] = process.argv.slice(2);
let config = {};
try {
  config = JSON.parse(fs.readFileSync(configPath, "utf8"));
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

config.gateway ||= {};
config.gateway.port = Number(port);
config.gateway.controlUi ||= {};
config.gateway.controlUi.allowedOrigins = originsRaw
  .split(",")
  .map((value) => value.trim())
  .filter(Boolean);

fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`, { mode: 0o600 });
NODE
fi

gateway_container_id="$(
  docker compose "${env_args[@]}" run -d \
    --service-ports \
    openclaw-local \
    openclaw gateway run --force
)"

docker compose "${env_args[@]}" up -d workspace-ui workspace-cms

cat <<EOF
ScienceClaw instance '${instance_name}' started.

Gateway container: ${gateway_container_id}
Gateway:          http://127.0.0.1:${gateway_port}
Workspace UI:     http://127.0.0.1:${workspace_ui_port}/lab?token=${workspace_ui_token}
Workspace CMS:    http://127.0.0.1:${cms_port}

Instance files:
  ${instance_root}
EOF
