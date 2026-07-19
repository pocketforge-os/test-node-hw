#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)
cd "$repo_root"

test_dir=$(mktemp -d)
trap 'rm -rf "$test_dir"' EXIT

fake_openscad="$test_dir/openscad"
printf '%s\n' \
  '#!/usr/bin/env bash' \
  "echo 'ERROR: synthetic parser failure' >&2" \
  'exit 0' >"$fake_openscad"
chmod 0755 "$fake_openscad"

set +e
diagnostics=$(OPENSCAD="$fake_openscad" scripts/lint-openscad.sh 2>&1)
status=$?
set -e

if (( status == 0 )); then
  printf '%s\n' "$diagnostics" >&2
  echo 'openscad_lint_test=fail reason=error_diagnostic_was_accepted' >&2
  exit 1
fi

grep -q 'reason=error_diagnostic' <<<"$diagnostics"
echo 'openscad_lint_test=pass case=zero_exit_with_error_diagnostic'
