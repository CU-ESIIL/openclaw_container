#!/usr/bin/env bash
set -Eeuo pipefail

workspace="${WORKSPACE_DIR:-/workspace}"
template_root="/opt/openclaw/seed-workspace"
force=0

usage() {
  cat <<'EOF'
Usage: init-working-group.sh [--workspace PATH] [--template-root PATH] [--force]

Create or refresh the scientific working group scaffold.

Default behavior is non-destructive: existing files are left untouched.
Use --force to overwrite existing starter files from the template root.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace)
      workspace="$2"
      shift 2
      ;;
    --template-root)
      template_root="$2"
      shift 2
      ;;
    --force)
      force=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ ! -d "${template_root}" ]; then
  echo "Template root not found: ${template_root}" >&2
  exit 1
fi

mkdir -p "${workspace}"

created_dirs=()
created_files=()
updated_files=()
skipped_files=()

ensure_dir() {
  local rel="$1"
  local dest="${workspace}/${rel}"
  if [ ! -d "${dest}" ]; then
    mkdir -p "${dest}"
    created_dirs+=("${rel}")
  fi
}

seed_file() {
  local rel="$1"
  local src="${template_root}/${rel}"
  local dest="${workspace}/${rel}"

  if [ ! -f "${src}" ]; then
    echo "Template file missing: ${src}" >&2
    exit 1
  fi

  mkdir -p "$(dirname "${dest}")"

  if [ -e "${dest}" ] && [ "${force}" -ne 1 ]; then
    skipped_files+=("${rel}")
    return
  fi

  if [ -e "${dest}" ] && [ "${force}" -eq 1 ]; then
    updated_files+=("${rel}")
  else
    created_files+=("${rel}")
  fi

  cp "${src}" "${dest}"
}

required_dirs=(
  "documents"
  "analysis"
  "figures"
  "literature"
  "meetings"
  "daily_notes"
  "agent_reports"
  "logs"
  "heartbeat"
  "soul"
  "prompts"
  "services"
  "services/pi_liaison"
  "scripts"
)

starter_files=(
  "README.md"
  "MEMORY.md"
  "AGENTS.md"
  "USER_CONTEXT.md"
  "PROJECT_INTAKE.md"
  "PROJECT_CHARTER.md"
  "TEAM_BRIEF.md"
  "INITIAL_TASKS.md"
  "QUESTIONS_FOR_USER.md"
  "ROADMAP.md"
  "DECISIONS.md"
  "ASSUMPTIONS.md"
  "HUMAN_REVIEW.md"
  "documents/README.md"
  "analysis/README.md"
  "figures/README.md"
  "literature/README.md"
  "meetings/README.md"
  "daily_notes/README.md"
  "agent_reports/README.md"
  "logs/README.md"
  "heartbeat/README.md"
  "soul/README.md"
  "prompts/README.md"
  "prompts/pi-liaison-startup.md"
  "services/README.md"
  "services/pi_liaison/README.md"
  "services/pi_liaison/.env.template"
  "scripts/README.md"
  "scripts/init-working-group.sh"
  "scripts/start-pi-liaison.sh"
  "scripts/check-secrets.sh"
  "scripts/mask-secrets.sh"
)

for dir in "${required_dirs[@]}"; do
  ensure_dir "${dir}"
done

for file in "${starter_files[@]}"; do
  seed_file "${file}"
done

chmod +x "${workspace}/scripts/init-working-group.sh" 2>/dev/null || true
chmod +x "${workspace}/scripts/start-pi-liaison.sh" 2>/dev/null || true
chmod +x "${workspace}/scripts/check-secrets.sh" 2>/dev/null || true
chmod +x "${workspace}/scripts/mask-secrets.sh" 2>/dev/null || true

echo "Scientific working group scaffold initialized at ${workspace}"
echo "Directories created: ${#created_dirs[@]}"
if [ "${#created_dirs[@]}" -gt 0 ]; then
  printf '  - %s\n' "${created_dirs[@]}"
fi
echo "Files created: ${#created_files[@]}"
if [ "${#created_files[@]}" -gt 0 ]; then
  printf '  - %s\n' "${created_files[@]}"
fi
echo "Files updated: ${#updated_files[@]}"
if [ "${#updated_files[@]}" -gt 0 ]; then
  printf '  - %s\n' "${updated_files[@]}"
fi
echo "Existing files left unchanged: ${#skipped_files[@]}"
