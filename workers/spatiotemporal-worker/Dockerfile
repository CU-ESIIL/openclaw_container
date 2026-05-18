FROM python:3.11-slim

ENV DATA_ROOT=/data
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gdal-bin \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        proj-bin \
        jq \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/scienceclaw-worker

COPY requirements-spatiotemporal.txt /tmp/requirements-spatiotemporal.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements-spatiotemporal.txt

COPY workers/spatiotemporal-worker/run_task.py /opt/scienceclaw-worker/run_task.py

WORKDIR /data/workspace

ENTRYPOINT ["python", "/opt/scienceclaw-worker/run_task.py"]
