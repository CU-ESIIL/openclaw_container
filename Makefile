.PHONY: help init-working-group doctor checkpoint test-working-group test-layout test-secrets

help:
	@echo "OASIS ScienceClaw commands"
	@echo
	@echo "  make init-working-group  Initialize the local workspace scaffold"
	@echo "  make doctor              Run safe local health checks"
	@echo "  make checkpoint          Write a local workspace checkpoint"
	@echo "  make test-working-group  Validate the seeded working-group scaffold"
	@echo "  make test-layout         Validate the /data layout scaffold"
	@echo "  make test-secrets        Check secret hygiene helpers"

init-working-group:
	@scripts/init_working_group.sh

doctor:
	@scripts/doctor.sh

checkpoint:
	@scripts/checkpoint.sh

test-working-group:
	@scripts/test-working-group.sh

test-layout:
	@scripts/test-scienceclaw-layout.sh

test-secrets:
	@scripts/test-secrets.sh

