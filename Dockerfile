FROM node:24-bookworm-slim

LABEL org.opencontainers.image.title="ScienceClaw"
LABEL org.opencontainers.image.description="AI-native environmental synthesis workspace built on OpenClaw."

ENV HOME=/root
ENV DATA_ROOT=/data
ENV OPENCLAW_CONFIG_DIR=/data/.openclaw
ENV OPENCLAW_AUTH_PROFILE_SECRET_DIR=/data/.openclaw/auth-profile-secrets
ENV OPENCLAW_WORKSPACE=/data/workspace
ENV EXTERNAL_STORAGE_ROOT=/external_storage
ENV SCIENCECLAW_CMS_PORT=8090
ENV OPENCLAW_DEFAULT_MODEL=codex/gpt-5.5
ENV OPENCLAW_GATEWAY_BIND=lan
ENV OPENCLAW_GATEWAY_PORT=18789
ENV OPENCLAW_CONTROL_ORIGINS=http://127.0.0.1:18789,http://localhost:18789
ENV WORKSPACE_UI_PORT=8888
ENV OPENCLAW_SEED_WORKSPACE=1
ENV OPENCLAW_INIT_WORKING_GROUP=1
ENV OPENCLAW_START_PI_LIAISON=1
ENV OPENCLAW_CONFIGURE_SLACK=1
ENV SCIENCECLAW_BRANDING=1
ENV SCIENCECLAW_PROJECT_TITLE="OASIS ScienceClaw Working Group"
ENV NODE_ENV=production
ARG OPENCLAW_VERSION=2026.5.18

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        build-essential \
        ca-certificates \
        curl \
        gdal-bin \
        ghostscript \
        git \
        gh \
        imagemagick \
        jq \
        geos-bin \
        libgeos-dev \
        libspatialindex-dev \
        libreoffice \
        nano \
        pandoc \
        poppler-utils \
        proj-bin \
        python3 \
        python3-pip \
        python3-venv \
        qpdf \
        ripgrep \
        rclone \
        sqlite3 \
        latexmk \
        lmodern \
        texlive-fonts-recommended \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-xetex \
        tini \
        tmux \
        tree \
        unzip \
        vim-tiny \
        wget \
    && rm -rf /var/lib/apt/lists/*

# OpenClaw's docs recommend Node 24 and support npm when Node is managed separately.
RUN npm install -g openclaw@${OPENCLAW_VERSION} \
    && npm cache clean --force

COPY requirements-spatiotemporal.txt /tmp/requirements-spatiotemporal.txt
RUN python3 -m pip install --break-system-packages --no-cache-dir \
        jupyterlab \
        playwright \
        uv \
    && python3 -m pip install --break-system-packages --no-cache-dir \
        -r /tmp/requirements-spatiotemporal.txt

WORKDIR /data/workspace

RUN mkdir -p /data/.openclaw/auth-profile-secrets /data/workspace /workspace /external_storage/local

COPY docker/entrypoint.sh /usr/local/bin/openclaw-container-entrypoint
COPY docker/service-entrypoint.sh /usr/local/bin/scienceclaw-service-entrypoint
COPY scripts/init-data-layout.sh /usr/local/bin/scienceclaw-init-data-layout
COPY scripts/openclaw-storage /usr/local/bin/openclaw-storage
COPY docker/seed-workspace /opt/openclaw/seed-workspace
COPY cms /opt/scienceclaw/cms
COPY storage /opt/scienceclaw/storage
COPY branding/control-ui /opt/scienceclaw/branding/control-ui
COPY docs/assets/brand /opt/scienceclaw/branding/assets
COPY scripts/install-control-ui-branding.sh /usr/local/bin/scienceclaw-install-control-ui-branding
COPY scripts/seed_file_manager_demo.py /usr/local/bin/scienceclaw-seed-file-manager-demo
RUN chmod +x /usr/local/bin/openclaw-container-entrypoint \
    && chmod +x /usr/local/bin/scienceclaw-service-entrypoint \
    && chmod +x /usr/local/bin/scienceclaw-init-data-layout \
    && chmod +x /usr/local/bin/openclaw-storage \
    && chmod +x /usr/local/bin/scienceclaw-install-control-ui-branding \
    && chmod +x /usr/local/bin/scienceclaw-seed-file-manager-demo \
    && chmod +x /opt/openclaw/seed-workspace/scripts/init-working-group.sh \
    && chmod +x /opt/openclaw/seed-workspace/scripts/start-pi-liaison.sh \
    && chmod +x /opt/openclaw/seed-workspace/scripts/check-secrets.sh \
    && chmod +x /opt/openclaw/seed-workspace/scripts/mask-secrets.sh \
    && chmod +x /opt/scienceclaw/cms/scienceclaw_cms.py \
    && chmod +x /opt/scienceclaw/storage/scripts/*.py

VOLUME ["/data", "/workspace", "/external_storage"]

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/openclaw-container-entrypoint"]
CMD ["/bin/bash"]
