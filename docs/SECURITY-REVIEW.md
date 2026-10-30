# Review scope and known limitations

Review date: 2026-10-30. Static checks of the inspiration project's binaries
included file formats, both executable architecture slices, signatures,
dependencies, imported symbols, strings and selected Intel disassembly. No
obvious malware indicators were observed in these checks. This was not exhaustive
reverse engineering, dynamic sandboxing, a vulnerability scan, or certification.

The original scanner frontend constructs a `system()` command using output
filenames in single quotes without escaping embedded single quotes. The Intel
binary contained the corresponding snprintf/system sequence. Specially crafted
filenames may cause shell command execution with the scanner user's privileges.
The scanner is excluded here. We do not allege malicious intent.

The original optional SANE library was ARM-only and dynamically depended on
Homebrew libusb, differing from the current static-link recipe. It is excluded.

For this distribution, hpcups was rebuilt locally from the HP-signed HPLIP source
archive. The verified primary fingerprint is:

```
82FF A7C6 AA74 11D9 34BD E173 AC69 536A 2CF3 A243
```

Published by HP at:
https://developers.hp.com/hp-linux-imaging-and-printing/hplipDigitalCertificate.html

The detached archive signature verifies through signing subkey:

```
1E3D 9B4E 4447 5F51 EC08 45AB 5E4E 4D24 A34E CD57
```

See `dist/signature.txt`. GnuPG's TRUST_UNDEFINED message refers to the local
web of trust; the primary fingerprint was compared explicitly with HP's page.
An initial keyserver download lacked user IDs and was rejected; the complete
key from HP's page was then used. No signature check was bypassed.

The resulting Intel filter depends dynamically only on system CUPS, CUPS image,
zlib, C++ and libSystem libraries. libjpeg-turbo is statically linked from the
existing Homebrew installation. That dependency and the compiler were not
independently rebuilt or fully audited. HP's signature does not cover them,
our build script, or the resulting macOS executable.

The local pipeline test converted a known PDF into CUPS raster and then PCL with
exit status zero. The owner subsequently confirmed successful physical printing
on HP 2376/macOS 26.6.2/Intel. We did not decode and compare every printed pixel,
test other models, or establish broad independent use.

The binary has an integrity-valid ad hoc signature, without Developer ID
identity or Apple notarization. Bundled SHA-256 checksums cannot protect against
an attacker replacing both artifacts and manifests. No guarantee of absence of
malware or vulnerabilities is made. Review code and rebuild if appropriate.

No private diagnostics, printer serial numbers, user screenshots, credentials,
or original machine logs are intentionally distributed in this repository.
