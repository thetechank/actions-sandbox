#!/usr/bin/env bash
# build.sh: the Riverton Tramways timetable bundle (github-actions/environments-and-gates.md).
#   timetable/build.sh OUT_DIR   checks timetable/lines.csv (six columns, times as HH:MM, a whole number
#                                of minutes between trams) and writes OUT_DIR/timetable.txt, one line
#                                per tram line; prints the bundle's line count and SHA-256
set -euo pipefail
out=${1:?usage: timetable/build.sh OUT_DIR}
src=$(dirname "$0")/lines.csv
mkdir -p "$out"
awk -F, 'NR == 1 { next }
  NF != 6 || $4 !~ /^[0-2][0-9]:[0-5][0-9]$/ || $5 !~ /^[0-2][0-9]:[0-5][0-9]$/ || $6 !~ /^[0-9]+$/ {
    printf "build: line %d of lines.csv is not LINE,FROM,TO,HH:MM,HH:MM,MINUTES\n", NR > "/dev/stderr"; bad = 1; next }
  { printf "Line %s  %s - %s  %s to %s, every %s min\n", $1, $2, $3, $4, $5, $6 }
  END { exit bad }' "$src" > "$out/timetable.txt"
echo "build: $(wc -l < "$out/timetable.txt" | tr -d ' ') lines, sha256=$(sha256sum "$out/timetable.txt" | cut -d' ' -f1)"
