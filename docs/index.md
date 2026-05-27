<section class="scienceclaw-title" markdown>
![ScienceClaw mark](assets/brand/scienceclaw.png){ .scienceclaw-title-logo }

# OASIS ScienceClaw

**ESIIL's multi-agent workspace**

Run an environmental synthesis workspace on your laptop, keep agent access narrow, and publish reviewed outputs without mixing private workspace files into the public site.
</section>

[Start here](start-here/index.md){ .md-button .md-button--primary }
[First 10 minutes](start-here/first-10-minutes.md){ .md-button }
[What is a container?](concepts/what-is-a-container.md){ .md-button }
[Launch locally](use/launch-locally.md){ .md-button }
[Template launch](use/template-github-launch.md){ .md-button }
[Where files go](use/where-files-go.md){ .md-button }
[Troubleshooting](troubleshooting.md){ .md-button }

<div class="grid cards" markdown>

- **Beginner-safe path**

  ---

  Learn the mental model first, then launch the container and do one small useful action.

- **Portable scientific workspace**

  ---

  Think of the container as a field station in a box: a reproducible set of tools for shared work.

- **Repo as memory**

  ---

  Keep decisions, assumptions, prompts, tasks, reports, and template improvements in versioned project memory.

- **Narrow, safer mounts**

  ---

  Mount only the folders agents need. Keep secrets local and large data in external storage.

- **Scientific working group**

  ---

  Use an 11-role environmental data science scaffold with a PI Liaison, shared memory, evidence standards, skeptic review, and human approval gates.

- **Visible outputs**

  ---

  Find figures, reports, logs, notebooks, maps, and provenance in predictable workspace folders.

- **Recoverable by design**

  ---

  Treat troubleshooting as normal work: checkpoint, inspect, recover, and avoid destructive commands.

- **Advanced when ready**

  ---

  Add model routing, storage backends, GitHub workflows, branded skins, and Kubernetes workers after the basics feel stable.

</div>

## Quick Win

```bash
cp .env.example .env
make init-working-group
make doctor
docker compose build
scripts/login-codex.sh
make checkpoint
```

The [First 10 Minutes](start-here/first-10-minutes.md) page gives the calm walkthrough. The [Glossary](reference/glossary.md) explains container terms without assuming command-line fluency.

Read [Security](security.md) before connecting Slack tokens to the PI Liaison.

For deeper work, continue to [Template GitHub Launch](use/template-github-launch.md), [OASIS ScienceClaw Template](oasis-template.md), [Model Routing](model-routing.md), [Storage](storage/index.md), [Publishing Workflow](publishing-workflow.md), and [Distributed Runtime](distributed-runtime.md).
