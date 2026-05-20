#!/usr/bin/env bash
set -Eeuo pipefail

config_dir="${OPENCLAW_CONFIG_DIR:-/root/.openclaw}"
config_path="${OPENCLAW_CONFIG_PATH:-${config_dir}/openclaw.json}"
workspace="${OPENCLAW_WORKSPACE:-/workspace}"
seed_dir="/opt/openclaw/seed-workspace"
data_root="${DATA_ROOT:-/data}"

if command -v scienceclaw-init-data-layout >/dev/null 2>&1; then
  scienceclaw-init-data-layout --data-root "${data_root}" >/tmp/scienceclaw-data-layout.log 2>&1 || {
    echo "ScienceClaw data layout initialization failed. Recent log:" >&2
    tail -n 80 /tmp/scienceclaw-data-layout.log >&2
    exit 1
  }
fi

if [ "${SCIENCECLAW_BRANDING:-1}" != "0" ] && command -v scienceclaw-install-control-ui-branding >/dev/null 2>&1; then
  scienceclaw-install-control-ui-branding >/tmp/scienceclaw-branding.log 2>&1 || {
    echo "ScienceClaw Control UI branding failed. Recent log:" >&2
    tail -n 80 /tmp/scienceclaw-branding.log >&2
    exit 1
  }
fi

mkdir -p \
  "${config_dir}" \
  "${config_dir}/auth-profile-secrets" \
  "${config_dir}/agents/main/sessions" \
  "${data_root}/logs" \
  "${workspace}"

if [ "${OPENCLAW_SEED_WORKSPACE:-1}" != "0" ] && [ -d "${seed_dir}" ]; then
  find "${seed_dir}" -type f | while IFS= read -r src; do
    rel="${src#${seed_dir}/}"
    dest="${workspace}/${rel}"
    mkdir -p "$(dirname "${dest}")"
    if [ ! -e "${dest}" ]; then
      cp "${src}" "${dest}"
    fi
  done
fi

if [ "${OPENCLAW_INIT_WORKING_GROUP:-1}" != "0" ]; then
  init_script="${workspace}/scripts/init-working-group.sh"
  if [ -f "${init_script}" ]; then
    chmod +x "${init_script}" || true
    "${init_script}" --workspace "${workspace}" --template-root "${seed_dir}"
  elif [ -f "${seed_dir}/scripts/init-working-group.sh" ]; then
    bash "${seed_dir}/scripts/init-working-group.sh" --workspace "${workspace}" --template-root "${seed_dir}"
  fi
fi

if [ "${SCIENCECLAW_BRANDING:-1}" != "0" ] && command -v scienceclaw-install-control-ui-branding >/dev/null 2>&1; then
  scienceclaw-install-control-ui-branding >/tmp/scienceclaw-branding.log 2>&1 || {
    echo "ScienceClaw Control UI branding failed. Recent log:" >&2
    tail -n 80 /tmp/scienceclaw-branding.log >&2
    exit 1
  }
fi

node <<'NODE'
const fs = require("fs");
const crypto = require("crypto");

const configPath = process.env.OPENCLAW_CONFIG_PATH || `${process.env.OPENCLAW_CONFIG_DIR || "/root/.openclaw"}/openclaw.json`;
const workspace = process.env.OPENCLAW_WORKSPACE || "/workspace";
const defaultModel = process.env.OPENCLAW_MODEL || process.env.OPENCLAW_DEFAULT_MODEL || "codex/gpt-5.5";
const gatewayBind = process.env.OPENCLAW_GATEWAY_BIND || "lan";
const gatewayPort = Number(process.env.OPENCLAW_GATEWAY_PORT || "18789");
const authMode = process.env.OPENCLAW_GATEWAY_AUTH_MODE || "token";
const origins = (process.env.OPENCLAW_CONTROL_ORIGINS || "http://127.0.0.1:18789,http://localhost:18789")
  .split(",")
  .map((value) => value.trim())
  .filter(Boolean);
const visibleRepliesMode = process.env.OPENCLAW_VISIBLE_REPLIES_MODE || "message_tool";

let config = {};
try {
  config = JSON.parse(fs.readFileSync(configPath, "utf8"));
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

config.agents ||= {};
config.agents.defaults ||= {};
config.agents.defaults.workspace = workspace;
config.agents.defaults.models ||= {};
config.agents.defaults.models[defaultModel] ||= {};
config.agents.defaults.model ||= {};
config.agents.defaults.model.primary = defaultModel;

config.gateway ||= {};
config.gateway.mode = "local";
config.gateway.bind = gatewayBind;
config.gateway.port = gatewayPort;
config.gateway.auth ||= {};
config.gateway.auth.mode = authMode;
if (authMode === "token") {
  config.gateway.auth.token =
    process.env.OPENCLAW_GATEWAY_TOKEN ||
    config.gateway.auth.token ||
    crypto.randomBytes(24).toString("hex");
}
config.gateway.controlUi ||= {};
config.gateway.controlUi.allowedOrigins = origins;

config.plugins ||= {};
config.plugins.entries ||= {};
config.plugins.entries.openai ||= {};
config.plugins.entries.openai.enabled = true;
config.plugins.entries.codex ||= {};
config.plugins.entries.codex.enabled = true;

config.messages ||= {};
delete config.messages.visibleReplies;
config.messages.groupChat ||= {};
config.messages.groupChat.visibleReplies = visibleRepliesMode;

config.meta ||= {};
config.meta.lastTouchedVersion ||= "container-bootstrap";

fs.mkdirSync(require("path").dirname(configPath), { recursive: true });
fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`, { mode: 0o600 });
NODE

chmod 700 "${config_dir}" || true
chmod 700 "${config_dir}/auth-profile-secrets" || true

if [ "${OPENCLAW_CONFIGURE_SLACK:-1}" != "0" ] \
  && [ -n "${SLACK_BOT_TOKEN:-}" ] \
  && [ -n "${SLACK_APP_TOKEN:-}" ]; then
  echo "Configuring Slack channel from environment-backed credentials..."
  openclaw channels add --channel slack --use-env --name pi-liaison >/tmp/openclaw-slack-configure.log 2>&1 || {
    echo "Slack channel configuration failed. Recent log:" >&2
    sed -E 's/(xoxb-|xapp-)[A-Za-z0-9._-]+/\1****REDACTED/g' /tmp/openclaw-slack-configure.log | tail -n 80 >&2
    exit 1
  }
fi

if [ "${OPENCLAW_START_PI_LIAISON:-1}" != "0" ]; then
  case "${1:-}" in
    /bin/bash|bash|/bin/sh|sh)
      liaison_script="${workspace}/scripts/start-pi-liaison.sh"
      if [ -x "${liaison_script}" ]; then
        exec "${liaison_script}"
      elif [ -f "${seed_dir}/scripts/start-pi-liaison.sh" ]; then
        exec bash "${seed_dir}/scripts/start-pi-liaison.sh"
      fi
      ;;
  esac
fi

exec "$@"
