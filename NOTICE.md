# Third-party notices

`dist/hpcups` was built locally from HP HPLIP 3.25.2, with an additional
`malloc.h` compatibility shim, endian/imageprocessor build flags, and static
linking to the existing Intel Homebrew libjpeg-turbo 3.2.0 library. No proprietary
HP binary plugin is included. The PPD comes from the same HPLIP archive, with its
filter path changed to `/Library/Printers/hplip-local/hpcups`.

HPLIP copyright and mixed BSD/MIT/GPL license terms are preserved in the source
archive and `licenses/HPLIP-COPYING`. Consult each source file for its terms.
The complete original source archive, detached signature and build recipe are
provided alongside the binary, rather than relying solely on a remote download.

libjpeg-turbo 3.2.0 copyright and terms: `licenses/libjpeg-turbo-LICENSE.md` and
`licenses/libjpeg-README.ijg`. This product includes software developed by the
Independent JPEG Group. Source: https://github.com/libjpeg-turbo/libjpeg-turbo/tree/3.2.0

The macOS build approach was informed by
https://github.com/squatchus/hp-deskjet-2320-macos-driver (MIT scripts). This
repository contains no scanner binary from that project and does not represent
its authors or claim their endorsement.
