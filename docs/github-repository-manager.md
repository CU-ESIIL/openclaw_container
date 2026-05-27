# GitHub Repository Manager

The ScienceClaw GitHub Repository Manager gives a running OpenClaw container controlled access to selected project repositories. It is not a manager for this container repository. The container repository defines the appliance; connected GitHub repositories are the scientific projects, manuscripts, data libraries, or collaboration spaces that the appliance is allowed to inspect or contribute to.

Open the manager from the ScienceClaw sidebar with **GitHub Auth**. The branded Control UI shows GitHub auth status and credential setup directly in the sidebar, with the full manager available for clone, branch, commit, push, and PR actions. It is also available directly at:

```text
http://127.0.0.1:8090/github
```

For additional instances, replace `8090` with that instance's CMS port.

## Operating Model

ScienceClaw uses an explicit allowlist. The manager does not discover every repository the user can access, and agents do not receive account-wide GitHub authority. A repository must be added to the local registry before ScienceClaw can clone or operate on it.

The default workflow is:

```text
authorized repository
  -> clone to /workspace/repos/
  -> create agent branch
  -> commit changes
  -> push working branch
  -> open pull request
  -> human review
```

Direct pushes to `main` and `master` are blocked by policy. Force pushes, branch deletion, tag deletion, automatic merging, and repository settings changes are not implemented.

## Authentication And Secrets

ScienceClaw is designed so a user can pull or build the container, provide local secrets, and start with GitHub access already available to both the OpenClaw agent runtime and the GitHub manager. GitHub credentials must come from environment variables or mounted secret files. They are not baked into the image and are not stored in the repository registry.

For organization work, use a fine-grained personal access token or GitHub App installation token scoped only to the repositories the working group should touch. The token should allow repository contents and pull requests as needed. Avoid account-wide classic tokens.

### GitHub CLI

Inside the container, run:

```bash
gh auth login
gh auth setup-git
gh auth status
```

This is the simplest interactive path for local use. The GitHub tab reports the sanitized `gh auth status` summary and never prints tokens.

### Fine-Grained Token Through Environment

Advanced users can provide `GITHUB_TOKEN` through `.env`, host secrets, Docker secrets, or deployment-specific secret storage. At startup, ScienceClaw also mirrors `GITHUB_TOKEN` to `GH_TOKEN` for GitHub CLI compatibility and runs `gh auth setup-git` when a token is available. That lets ordinary `git push` and `gh pr create` work from inside the container without an interactive login.

Tokens are not written to the registry, logs, Markdown files, screenshots, or prompt logs.

### Docker Secret File

For the intended reusable-container workflow, keep secrets outside git and mount them into the container:

```bash
mkdir -p secrets
printf '%s\n' 'github_pat_or_fine_grained_token' > secrets/github_token
chmod 600 secrets/github_token
docker compose -f docker-compose.yml -f docker-compose.secrets.yml up -d
```

The overlay mounts the token at `/run/secrets/github_token` and sets `GITHUB_TOKEN_FILE` and `GH_TOKEN_FILE` for both the OpenClaw gateway service and the workspace CMS. The entrypoint reads the first line of the secret file, exports it in-process, and configures GitHub CLI for git credential use.

Spawned instances use the same overlay automatically when `secrets/github_token` exists, when `SCIENCECLAW_GITHUB_TOKEN_FILE` points at a token file, or when `SCIENCECLAW_USE_SECRETS_OVERLAY=1` is set:

```bash
SCIENCECLAW_GITHUB_TOKEN_FILE=./secrets/github_token \
scripts/start-instance.sh project-three 18791 8890 8092
```

In the GitHub manager, click **Configure git credentials** after adding or rotating a token. The button reruns the GitHub CLI credential setup inside the CMS process and reports sanitized status output. It is a browser approval/action path and does not require `/approve`.

For the current gateway 3 prototype, the repeatable authentication path is:

```bash
mkdir -p secrets
printf '%s\n' 'PASTE_YOUR_FINE_GRAINED_TOKEN_HERE' > secrets/github_token
chmod 600 secrets/github_token

SCIENCECLAW_GITHUB_TOKEN_FILE=./secrets/github_token \
SCIENCECLAW_USE_SECRETS_OVERLAY=1 \
scripts/start-instance.sh project-three 18791 8890 8092
```

Then open the gateway 3 Control UI, expand **GitHub Auth** in the ScienceClaw sidebar, and click **Configure git credentials**. The status panel should report that a token file is visible and that GitHub CLI/git credential setup is available. Add repositories by `owner/repo`; the cloned path shown in the sidebar is the same `/workspace/repos/<repo>` path the agents should use.

Use a fine-grained token scoped only to the working-group repositories. Grant repository contents read/write when the group needs branch pushes, and pull request read/write when the group should open PRs. Do not commit the token file, paste the token into chat, or store it in the repository registry.

### GitHub Actions / Self-Hosted Runner

For a GitHub-managed launch, add the repository secrets listed in `docs/security-and-credentials.md`, then run the manual **ScienceClaw runtime from secrets** workflow. Use a self-hosted runner for a durable Gateway. The workflow accepts the recommended `SCIENCECLAW_...` secret names and common local `.env` aliases for Verde and Slack. GitHub repository write access still requires `SCIENCECLAW_GITHUB_TOKEN`, which should be a fine-grained token scoped only to the working-group repositories. The workflow materializes the secrets only on the runner, starts ScienceClaw with the same instance helper, and smoke-tests OpenClaw plus the CMS GitHub status endpoint.

By default, the workflow also authorizes and clones the launch repository itself. For a template or forked repository, that means the new project repository appears in `/workspace/repos/<repo>` immediately, and humans and agents can use the GitHub manager to branch, commit, push, and open pull requests back to that same repository. Additional repositories can be added later from the GitHub manager.

### Future GitHub App Path

GitHub App authentication is the preferred long-term model because it supports selected-repository installation, revocation, organization-friendly permissions, and least-privilege access. This first implementation documents that direction but does not require GitHub App setup.

## Registry

Authorized repositories are stored in:

```text
/workspace/.openclaw-github/authorized-repos.yaml
```

Example:

```yaml
repositories:
  - owner: "CU-ESIIL"
    repo: "WUI_boundary"
    url: "https://github.com/CU-ESIIL/WUI_boundary.git"
    local_path: "/workspace/repos/WUI_boundary"
    default_branch: "main"
    permission_tier: "contribute"
    enabled: true
    notes: "Wildfire WUI boundary project repository"
```

The registry stores repository metadata only. It must not contain tokens.

## Permission Tiers

| Tier | Behavior |
| --- | --- |
| `read` | Clone, fetch, inspect files, inspect branches, and view local status. No commits, pushes, or PR creation. |
| `contribute` | Create working branches, commit local changes, push branches, and open pull requests. Direct push to protected branches remains blocked. |
| `admin` | Reserved for future use and treated conservatively in this first implementation. |

## Local Clone Layout

Repositories clone into:

```text
/workspace/repos/
```

The manager validates clone destinations so they cannot escape this directory. From the GitHub tab, use **Open in Files** to inspect a cloned repository in the workspace file manager.

## Branch And PR Safety

Contribute operations use explicit git and GitHub CLI commands with argument arrays, not arbitrary shell strings. Branch names, repository names, paths, PR titles, and commit messages are validated or passed as arguments.

Commits created through the manager include this attribution footer:

```text
Generated with OpenClaw in the ScienceClaw/OASIS container.
Human review required before merge.
```

Pull request bodies include the same attribution. If tests were not run, the PR body should say `Tests not run.`

## Smoke Test

Run:

```bash
make github-smoke-test
```

The test checks that git is available, that GitHub CLI is either available on the host or installed in the container image, that the registry can be written and parsed, that invalid repository names and path escapes are rejected, that protected branches are blocked by policy, and that the GitHub status endpoint returns safe JSON.
