# HP DeskJet 2376 USB printing on macOS

Community print-only package. **Physically tested by its owner on one HP DeskJet
Ink Advantage 2376, Intel MacBook Pro, macOS 26.6.2, on October 30, 2026.**
No HP affiliation. No Apple Silicon binary, scanner, firmware update or background
service. Other devices and macOS releases have not been validated.

The printer was detected as DeskJet 2300 series but used a generic laser PCL
driver. HP Easy Start's catalogue returned `NOT SUPPORTED` for this combination
and no suitable PPD. The locally built hpcups filter solved this particular case.

## Install

Download/extract this repository, or clone it:

```bash
git clone https://github.com/guistela/hp-deskjet-2376-macos-driver.git
cd hp-deskjet-2376-macos-driver
(cd dist && shasum -a 256 -c install.sha256)
cat scripts/install.sh
bash scripts/install.sh
```

Use an interactive macOS Terminal. Connect and power on the printer, and load
paper. The installer requests administrator authentication and submits **one
colour test page**. Choose **HP DeskJet 2376 (driver local)** in print dialogs.
An empty queue alone does not prove a successful physical print.

Only `/Library/Printers/hplip-local/` and queue `HP_DeskJet_2376_Local` are installed.
Other queues and the default printer are preserved. No quarantine removal,
downloads during install, or security-setting changes. Disconnect other
DeskJet 2300 printers during setup to avoid selecting the wrong device.

## Build and test

Requires Intel macOS 26, Xcode Command Line Tools, Python 3, GnuPG, and an Intel
Homebrew libjpeg-turbo installation under `/usr/local/opt/jpeg-turbo`.

```bash
brew install gnupg jpeg-turbo
python3 scripts/build.py
bash scripts/test.sh
```

The HP-signed HPLIP 3.25.2 archive, signature and pinned official public key are
included in `sources/`. The build uses SDK CUPS headers and statically links the
locally installed JPEG library. It does not reuse the inspiration project's
precompiled binaries. Different SDK/compiler/JPEG versions may produce different
bytes; bit-for-bit reproducibility is not claimed. This pinned version is the
tested baseline, not a claim that it is latest or free of vulnerabilities.

## Security and provenance

Read [docs/SECURITY-REVIEW.md](docs/SECURITY-REVIEW.md). The executable is ad hoc
signed, not Developer ID signed or Apple notarized. Checksums provide integrity
relative to the included manifest, not independent publisher authentication.
The HP signature authenticates HPLIP sources, not the macOS port or build tools.
Static inspection was partial, not a malware-free certification. The scanner
was excluded after finding unsafe shell interpolation in its published frontend.
This is not evidence of malicious intent. No broad independent adoption is claimed.

## Uninstall and report problems

```bash
bash scripts/uninstall.sh
```

For issues, include model, CPU architecture, macOS version, error messages and
whether paper physically printed. Redact serial numbers and personal data.
PPD paper-name warnings and CUPS legacy-driver deprecation warnings appeared
during the successful installation. They did not prevent that test.

Credits: [HP HPLIP](https://developers.hp.com/hp-linux-imaging-and-printing),
[squatchus' macOS port recipe](https://github.com/squatchus/hp-deskjet-2320-macos-driver),
and [libjpeg-turbo](https://libjpeg-turbo.org/). Prepared with OpenAI Codex
assistance and physically tested by the owner. First-party scripts/docs: MIT.
Third-party licensing is preserved in `NOTICE.md`, `licenses/`, and `sources/`.
Provided without warranty. See Portuguese README for full operational details.
