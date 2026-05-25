# INITIAL_TASKS.md

## Continuous Improvement Loop (CI Loop)
- Triggered by cron:33f64e7a-8d8f-4121-955c-8ec289ea54e0
- Objective: Each agent reviews its own manuscript/code, improves modularity, optimizes performance, tightens narrative for novice and expert readers, identifies gaps, proposes new simulations or hypotheses, discusses with the team, and commits any agreed edits.
- Frequency: Runs at each heartbeat (periodic).
- Process:
  1. PI Liaison notifies all agents of CI Loop start.
  2. Each agent performs self-review and records findings in `agent_reports/`.
  3. Agents propose edits via `edit` tool or create pull requests (pending human approval).
  4. Agents discuss findings via `TEAM_BRIEF.md` and resolve conflicts.
  5. Consolidated updates are committed to the repository.
  6. PI Liaison updates `PROJECT_CHARTER.md` and `TEAM_BRIEF.md` with status.

## Next Steps
- PI Liaison will broadcast the CI Loop start message to the team.
- Agents will begin their reviews and report back within the next hour.
- Upon completion, a summary will be posted here.
