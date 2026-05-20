# Launch Locally

This page is for running OASIS ScienceClaw on your own machine.

## Prerequisites

- Docker Desktop or a compatible Docker engine.
- Git.
- A local checkout of this repository.
- Optional model or integration credentials in `.env`.

## Start

```bash
cp .env.example .env
docker compose up --build
```

After the first build, use:

```bash
docker compose up
```

## Stop

```bash
docker compose down
```

This stops services. It does not automatically delete named volumes.

## Check Running Services

```bash
docker compose ps
```

## Common Local Interfaces

| Interface | Typical Use |
| --- | --- |
| OpenClaw Control UI | Chat, agents, sessions, gateway status |
| JupyterLab | Browse and edit workspace files |
| Workspace CMS | Review and promote reports into public docs |

If a port is already in use, start a second instance with the instance helper or adjust the port variables in `.env`.

!!! warning "Mount narrowly"
    Mount only the folders the working group needs. Avoid mounting your whole home directory into an agent-accessible container.

