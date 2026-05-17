FROM node:24-bookworm-slim

LABEL org.opencontainers.image.title="OpenClaw Local Docker"
LABEL org.opencontainers.image.description="Local OpenClaw CLI image with persisted config and workspace mounts."

ENV HOME=/root
ENV OPENCLAW_CONFIG_DIR=/root/.openclaw
ENV OPENCLAW_AUTH_PROFILE_SECRET_DIR=/root/.openclaw/auth-profile-secrets
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

VOLUME ["/root/.openclaw", "/workspace"]

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/bash"]
