#!/usr/bin/env bash
# preview.sh: the Spoke & Sprocket repair café's rota preview (github-actions/security-hardening.md §5).
# Prints the Saturday shifts in volunteers/rota.csv, one line each, for the sign-up bot's comment.
set -eu
echo "Rota preview ($(($(wc -l < volunteers/rota.csv) - 1)) shifts):"
tail -n +2 volunteers/rota.csv | while IFS=, read -r date shift volunteer skill; do
  echo "- $date $shift: $volunteer ($skill)"
done
