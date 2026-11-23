#!/usr/bin/env bash
# preview.sh as a pull request changes it (github-actions/security-hardening.md §5): the stand-in for
# hostile code. It prints the preview as before, then reports what it can reach: the secret the job
# put in its environment (its length only) and the job's token (it tries to write a comment with it).
# Harmless here, but code that can do this can also send the secret anywhere.
set -eu
echo "Rota preview ($(($(wc -l < volunteers/rota.csv) - 1)) shifts):"
tail -n +2 volunteers/rota.csv | while IFS=, read -r date shift volunteer skill; do
  echo "- $date $shift: $volunteer ($skill)"
done
if [ -n "${SIGNUP_KEY:-}" ]; then
  echo "pr code: LAB_FAKE_SIGNUP_KEY has ${#SIGNUP_KEY} characters"
else
  echo "pr code: no LAB_FAKE_SIGNUP_KEY in its environment"
fi
if [ -n "${GH_TOKEN:-}" ] && [ -n "${PR:-}" ] &&
  gh api -X POST "repos/$GITHUB_REPOSITORY/issues/$PR/comments" -f body='Written by the pull request'"'"'s own code with the job'"'"'s token.' > /dev/null; then
  echo "pr code: wrote a comment on PR #$PR with the job's token"
else
  echo "pr code: could not write a comment"
fi
