#!/bin/bash
# Offline conversion test. Does not submit jobs or access the USB printer.
set -euo pipefail
TASK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$TASK_ROOT/dist"
WORK="$(mktemp -d /private/tmp/hp-print-test.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT
cd "$BUILD"
shasum -a 256 -c install.sha256
codesign --verify --strict hpcups
cupstestppd -I filters HP-DeskJet-2376.ppd > "$WORK/ppd.log"
cupsfilter -p HP-DeskJet-2376.ppd -i application/pdf -m application/vnd.cups-raster \
    -o PageSize=A4 test-colors.pdf > "$WORK/page.raster" 2> "$WORK/raster.log"
PPD="$BUILD/HP-DeskJet-2376.ppd" "$BUILD/hpcups" 1 local offline-test 1 \
    'PageSize=A4' "$WORK/page.raster" > "$WORK/page.pcl" 2> "$WORK/filter.log"
test -s "$WORK/page.pcl"
echo "Offline PDF → raster → PCL conversion passed ($(wc -c < "$WORK/page.pcl") bytes)."
echo 'This does not validate physical printing or pixel accuracy.'
