#!/bin/bash
# Install only the locally compiled print filter and create a separate queue.
set -euo pipefail
TASK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$TASK_ROOT/dist"
QUEUE=HP_DeskJet_2376_Local
if [ "$(uname -m)" != x86_64 ] || [ "$(sysctl -in sysctl.proc_translated 2>/dev/null || true)" = 1 ]; then
    echo 'This package supports Intel Macs only; Apple Silicon is not supported.' >&2
    exit 1
fi
if [ "$(sw_vers -productVersion | cut -d. -f1)" != 26 ]; then
    echo 'This package was built and tested for macOS 26 only.' >&2
    exit 1
fi
if [ "$(id -u)" -ne 0 ]; then
    exec /usr/bin/sudo /bin/bash "$0"
fi
cd "$BUILD"
/usr/bin/shasum -a 256 -c install.sha256
/usr/bin/codesign --verify --strict hpcups
# Require the expected family, rather than selecting any attached DeskJet.
URI="$(/usr/libexec/cups/backend/usb | /usr/bin/awk '$1=="direct" && tolower($2) ~ /^usb:\/\/hp\/deskjet(%20| )?2300/ {print $2; exit}')"
if [ -z "$URI" ]; then
    echo 'HP DeskJet 2300 não encontrada no USB. Ligue e conecte a impressora.' >&2
    exit 1
fi
/usr/bin/install -d -o root -g wheel -m 755 /Library/Printers/hplip-local
/usr/bin/install -o root -g wheel -m 755 hpcups /Library/Printers/hplip-local/hpcups
/usr/bin/install -o root -g wheel -m 644 HP-DeskJet-2376.ppd /Library/Printers/hplip-local/HP-DeskJet-2376.ppd
/usr/bin/cupstestppd /Library/Printers/hplip-local/HP-DeskJet-2376.ppd
/usr/sbin/lpadmin -p "$QUEUE" -v "$URI" \
    -P /Library/Printers/hplip-local/HP-DeskJet-2376.ppd \
    -D 'HP DeskJet 2376 (driver local)' -L USB \
    -o PageSize=A4 -o printer-is-shared=false -o printer-error-policy=stop-printer -E
/usr/bin/lpstat -p "$QUEUE" -v "$QUEUE"
echo 'Driver instalado. Enviando uma página de teste com quatro retângulos coloridos.'
/usr/bin/lp -d "$QUEUE" -t 'Teste HP 2376' -o PageSize=A4 "$BUILD/test-colors.pdf"
echo 'Confira se a folha saiu. Se sair, selecione HP DeskJet 2376 (driver local) ao imprimir.'
