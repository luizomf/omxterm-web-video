#!/usr/bin/env bash

set -Eeuo pipefail

readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SETUP_SCRIPT="${ROOT_DIR}/scripts/setup_omxterm_web"
readonly CONFIG_EXAMPLE="${ROOT_DIR}/scripts/setup_omxterm_web.env.example"
readonly PIN_PATTERN='^traefik:v[0-9]+\.[0-9]+\.[0-9]+@sha256:[0-9a-f]{64}$'

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

extract_single_pin() {
  local file=$1
  local pattern=$2
  local label=$3
  local matches

  matches="$(sed -n "$pattern" "$file")"
  [[ -n "$matches" ]] || fail "could not find the Traefik image in ${label}"
  [[ "$matches" != *$'\n'* ]] || fail "found multiple Traefik image values in ${label}"
  printf '%s' "$matches"
}

setup_pin="$(extract_single_pin \
  "$SETUP_SCRIPT" \
  's/^  OMXTERM_TRAEFIK_IMAGE="${OMXTERM_TRAEFIK_IMAGE:-\([^\"]*\)}"$/\1/p' \
  'scripts/setup_omxterm_web')"
example_pin="$(extract_single_pin \
  "$CONFIG_EXAMPLE" \
  "s/^OMXTERM_TRAEFIK_IMAGE='\\([^']*\\)'$/\\1/p" \
  'scripts/setup_omxterm_web.env.example')"

[[ "$setup_pin" == "$example_pin" ]] || {
  fail 'the setup default and public example use different Traefik images'
}

[[ "$setup_pin" =~ $PIN_PATTERN ]] || {
  fail 'the Traefik image must use traefik:vX.Y.Z plus a full lowercase SHA-256 digest'
}

printf 'PASS: synchronized immutable Traefik image pin\n'
