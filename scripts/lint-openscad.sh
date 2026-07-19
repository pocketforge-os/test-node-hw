#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)
cd "$repo_root"

mapfile -d '' sources < <(
  find . -type f -name '*.scad' -not -path './.git/*' -print0 | sort -z
)

if (( ${#sources[@]} == 0 )); then
  echo 'openscad_lint=fail reason=no_sources' >&2
  exit 1
fi

lint_dir=$(mktemp -d)
trap 'rm -rf "$lint_dir"' EXIT

openscad_bin=${OPENSCAD:-openscad}
for index in "${!sources[@]}"; do
  source=${sources[$index]}
  echo "openscad_lint_source=$source"
  if ! diagnostics=$(
    "$openscad_bin" \
      --hardwarnings \
      --check-parameters=true \
      --check-parameter-ranges=true \
      -o "$lint_dir/$index.csg" \
      "$source" 2>&1
  ); then
    printf '%s\n' "$diagnostics" >&2
    echo "openscad_lint=fail source=$source reason=nonzero_exit" >&2
    exit 1
  fi
  printf '%s\n' "$diagnostics"
  if grep -q '^ERROR:' <<<"$diagnostics"; then
    echo "openscad_lint=fail source=$source reason=error_diagnostic" >&2
    exit 1
  fi
done

echo "openscad_lint=pass sources=${#sources[@]}"
