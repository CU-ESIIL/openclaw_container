FROM node:24-bookworm-slim

LABEL org.opencontainers.image.title="OpenClaw Local Docker"
LABEL org.opencontainers.image.description="Local OpenClaw CLI image with persisted config and workspace mounts."

ENV HOME=/root
ENV OPENCLAW_CONFIG_DIR=/root/.openclaw
ENV OPENCLAW_AUTH_PROFILE_SECRET_DIR=/root/.openclaw/auth-profile-secrets
ENV OPENCLAW_DEFAULT_MODEL=codex/gpt-5.5
ENV OPENCLAW_GATEWAY_BIND=lan
ENV OPENCLAW_GATEWAY_PORT=18789
ENV OPENCLAW_CONTROL_ORIGINS=http://127.0.0.1:18789,http://localhost:18789
ENV OPENCLAW_SEED_WORKSPACE=1
ENV OPENCLAW_INIT_WORKING_GROUP=1
ENV OPENCLAW_START_PI_LIAISON=1
ENV OPENCLAW_CONFIGURE_SLACK=1
ENV NODE_ENV=production

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        tini \
    && rm -rf /var/lib/apt/lists/*

# OpenClaw's docs recommend Node 24 and support npm when Node is managed separately.
RUN npm install -g openclaw@latest \
    && npm cache clean --force

WORKDIR /workspace

RUN mkdir -p /root/.openclaw/auth-profile-secrets /workspace

COPY docker/entrypoint.sh /usr/local/bin/openclaw-container-entrypoint
COPY docker/seed-workspace /opt/openclaw/seed-workspace
RUN chmod +x /usr/local/bin/openclaw-container-entrypoint \
    && chmod +x /opt/openclaw/seed-workspace/scripts/init-working-group.sh \
    && chmod +x /opt/openclaw/seed-workspace/scripts/start-pi-liaison.sh \
    && chmod +x /opt/openclaw/seed-workspace/scripts/check-secrets.sh \
    && chmod +x /opt/openclaw/seed-workspace/scripts/mask-secrets.sh

VOLUME ["/root/.openclaw", "/workspace"]

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/openclaw-container-entrypoint"]
CMD ["/bin/bash"]
