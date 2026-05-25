# MODEL_ASSIGNMENTS.md - Role-Based Model Routing

This register documents which model route each working-group role should use by default and where open-model API experiments are allowed.

Do not store API keys, OAuth callback URLs, access tokens, refresh tokens, provider secrets, or billing credentials in this file. Keep credentials in the local `.env` file or in OpenClaw's local auth store.

## Default Policy

- Use `verde/js2/gpt-oss-120b` for all working-group roles while Codex token availability is constrained, per PI request on 2026-05-18.
- The PI Liaison / User Interview Agent and Scientific Director may be moved back to a high-reliability Codex/OpenAI route when token availability returns.
- Use open-model API experiments first for bounded specialist work, such as data inventories, literature triage, first-pass skeptic questions, and internal memos.
- Do not change the default model for the PI Liaison, Scientific Director, or Slack-facing route without human approval.
- Record model changes, evaluation notes, failures, and reversions in `DECISIONS.md` or `agent_reports/model_evaluations.md`.
- Never use an unevaluated model route for publication approval, sensitive claims, irreversible filesystem actions, credential changes, or external messaging.

## Assignment Table

| Role | Default route | Open-model API experiments | Notes |
| --- | --- | --- | --- |
| PI Liaison / User Interview Agent | `verde/js2/gpt-oss-120b` | Yes | Human-facing, Slack-facing, and responsible for question batching. Moved to Verde by PI request on 2026-05-18 due to Codex token constraints. |
| Scientific Director | `verde/js2/gpt-oss-120b` | Yes | Responsible for scientific direction and claim promotion. Moved to Verde by PI request on 2026-05-18 due to Codex token constraints. |
| Deputy Director / Integrator | `verde/js2/gpt-oss-120b` | Yes | Must preserve coherence across roles. |
| Data Engineer / Infrastructure Scientist | `verde/js2/gpt-oss-120b` | Yes | Good candidate for bounded data inventory and reproducibility checks. |
| Quantitative Modeler | `verde/js2/gpt-oss-120b` | Yes | Use for scaffold review and diagnostics; human review for modeling decisions. |
| Domain Scientist | `verde/js2/gpt-oss-120b` | Yes | Must cite evidence and flag uncertainty. |
| Scientific Narrative Lead | `verde/js2/gpt-oss-120b` | Yes | Use for internal drafts, not final claims. |
| Technical Communicator | `verde/js2/gpt-oss-120b` | Yes | Good candidate for summaries and README-style drafts. |
| Citation & Evidence Curator | `verde/js2/gpt-oss-120b` | Yes | Must preserve citation provenance and avoid invented citations. |
| Skeptic / Adversarial Reviewer | `verde/js2/gpt-oss-120b` | Yes | Useful for second opinions; findings still need evidence checks. |
| Societal Impact / Translation Agent | `verde/js2/gpt-oss-120b` | Yes, with sensitivity limits | Sensitive community, policy, public-health, legal, or sovereignty claims still require human review. |

## Open-Model API Placeholders

If a provider such as Verde exposes an OpenAI-compatible API endpoint, put local credentials in `.env` and keep them out of git:

```dotenv
VERDE_LLM_BASE_URL=
VERDE_LLM_API_KEY=
VERDE_LLM_DEFAULT_MODEL=
VERDE_LLM_PROVIDER_NAME=verde
```

The active OpenClaw provider registration is in the local OpenClaw config, with credentials sourced from the environment or local auth store. The current configured route is `verde/js2/gpt-oss-120b` via `https://llm-api.cyverse.ai/v1`.

## Evaluation Checklist

Before promoting a model route from experiment to default:

1. Run a bounded task with known expected behavior.
2. Check whether the model follows the role limits in `AGENTS.md`.
3. Check whether it preserves citations and avoids invented sources.
4. Check whether it asks for human review when required by `HUMAN_REVIEW.md`.
5. Compare outputs against the current high-reliability route.
6. Record the result in `agent_reports/model_evaluations.md` or `DECISIONS.md`.

## Failure Modes To Watch

- Inventing citations, datasets, approvals, or user preferences.
- Treating Slack as permission to execute arbitrary shell commands.
- Ignoring `QUESTIONS_FOR_USER.md` and interrupting the user directly.
- Making strong scientific, policy, community, legal, public-health, or sovereignty claims without review.
- Silently using external APIs that create cost, data-transfer, or licensing issues.
