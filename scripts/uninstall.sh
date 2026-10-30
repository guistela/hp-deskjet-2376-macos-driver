#!/bin/bash
set -euo pipefail
if [ "$(id -u)" -ne 0 ]; then
    exec /usr/bin/sudo /bin/bash "$0"
fi
QUEUE=HP_DeskJet_2376_Local
if /usr/bin/lpstat -p "$QUEUE" >/dev/null 2>&1; then
    /usr/sbin/lpadmin -x "$QUEUE"
fi
/bin/rm -f /Library/Printers/hplip-local/hpcups /Library/Printers/hplip-local/HP-DeskJet-2376.ppd
/bin/rmdir /Library/Printers/hplip-local 2>/dev/null || true
echo 'Local HP 2376 queue and print driver removed.'
