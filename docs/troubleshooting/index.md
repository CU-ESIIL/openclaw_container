# Troubleshooting And Recovery

Troubleshooting is normal. It does not mean the project is broken.

Start with the symptom closest to what you see.

| Symptom | What Probably Happened | First Safe Check |
| --- | --- | --- |
| Container will not start | Port, build, or environment issue | `docker compose ps` |
| I cannot find my files | Looking in runtime instead of mounted workspace | Read [Where Files Go](../use/where-files-go.md) |
| API key is not working | Missing or rotated secret | `scripts/check-secrets.sh` |
| GitHub is not connected | Auth or remote issue | `git status` |
| Storage is not connected | Credentials, endpoint, or path mismatch | Review [Storage](../storage/index.md) |
| UI looks wrong | Browser cache or branding asset mismatch | Hard refresh the page |
| Restart lost state | State was only inside the container runtime | Check repo, volumes, mounted workspace |
| I think I broke it | Local change or stale container | Checkpoint, then inspect `git status` |

## Safe First Commands

```bash
git status
docker compose ps
make doctor
scripts/status.sh
scripts/test-working-group.sh
```

## What Not To Do First

- Do not delete volumes until you know what they contain.
- Do not run `git reset --hard` unless you intentionally want to discard local work.
- Do not paste secrets into chat, screenshots, markdown files, or issues.
- Do not mount your whole home directory to "fix" a missing file.

## When To Ask For Help

Ask for help when:

- credentials may have been exposed,
- data might be sensitive or restricted,
- a command would delete or overwrite files,
- you do not know whether a file belongs in git,
- a model or agent is recommending publication or policy claims.
