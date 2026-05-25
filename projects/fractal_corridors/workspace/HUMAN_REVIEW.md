# HUMAN_REVIEW.md

Human approval is required before any agent performs or finalizes the actions below.

## Always Require Approval

- Deleting files or directories
- Pushing to GitHub or another remote
- Installing third-party OpenClaw skills, plugins, packages, or system tools
- Mounting new host folders into the container
- Sending emails, messages, posts, or other external communications
- Modifying credentials, tokens, auth profiles, API keys, or secrets
- Publishing web pages, reports, datasets, figures, or public documentation
- Making claims about communities, Tribes, Indigenous knowledge, public health, legal rules, or policy recommendations
- Running expensive or long jobs
- Using external APIs with billing implications

## Review Expectations

Approval should include the specific action, target files or services, expected cost or risk, and rollback plan when relevant. Silence is not approval.

## Why This Exists

Autonomous agents may have file, shell, network, and tool access. This workspace uses bounded roles and review gates to reduce risk, but it does not guarantee safe autonomy. Human judgment remains part of the workflow.
