#!/usr/bin/env python3
"""Build only hpcups from the HP-signed source archive. Never installs."""
from pathlib import Path
import gzip
import hashlib
import os
import re
import subprocess
import tempfile
import tarfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources'
OUTPUT = ROOT / 'dist'
FINGERPRINT = '82FFA7C6AA7411D934BDE173AC69536A2CF3A243'


def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='hp-key-', dir='/private/tmp') as keys:
        os.chmod(keys, 0o700)
        base = ['gpg', '--homedir', keys, '--batch', '--no-autostart']
        pubkey = SOURCE / 'hp-official-publickey.asc'
        result = run(base + ['--with-colons', '--show-keys', pubkey], capture_output=True, text=True)
        fingerprint = next(line.split(':')[9] for line in result.stdout.splitlines() if line.startswith('fpr:'))
        assert fingerprint == FINGERPRINT, 'Unexpected HP public key'
        run(base + ['--import', pubkey], capture_output=True)
        result = run(base + ['--status-fd', '1', '--verify', SOURCE / 'hplip-3.25.2.tar.gz.asc',
                             SOURCE / 'hplip-3.25.2.tar.gz'], capture_output=True, text=True)
        assert any(line.startswith('[GNUPG:] VALIDSIG ') and line.split()[-1] == FINGERPRINT
                   for line in result.stdout.splitlines()), 'Expected HP signature missing'
        (OUTPUT / 'signature.txt').write_text(result.stdout + result.stderr)
    archive = SOURCE / 'hplip-3.25.2.tar.gz'
    (OUTPUT / 'source.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '\n')
    with tempfile.TemporaryDirectory(prefix='hp-compile-', dir='/private/tmp') as work:
        work = Path(work)
        with tarfile.open(archive) as tar:
            for entry in tar.getmembers():
                target = (work / entry.name).resolve()
                assert target.is_relative_to(work) and not entry.issym() and not entry.islnk(), 'Unsafe archive member'
            tar.extractall(work)
        src = work / 'hplip-3.25.2'
        shim = src / 'shim'
        shim.mkdir()
        (shim / 'malloc.h').write_text('#pragma once\n#include <stdlib.h>\n')
        sdk = subprocess.check_output(['xcrun', '--show-sdk-path'], text=True).strip()
        jpeg = Path('/usr/local/opt/jpeg-turbo')
        assert (jpeg / 'lib/libjpeg.a').is_file(), 'Intel libjpeg static library missing'
        common = ['-arch', 'x86_64', '-isysroot', sdk, '-O2', '-w', '-DAPDK_LITTLE_ENDIAN',
                  '-DDISABLE_IMAGEPROCESSOR', '-DVERSION="3.25.2"', '-I.', '-Ishim',
                  '-Iprnt/hpcups', '-Icommon', '-Iio/hpmud', '-I' + str(jpeg / 'include'),
                  '-Iprnt/hpijs']
        makefile = (src / 'Makefile.am').read_text()
        block = makefile.split('hpcups_SOURCES', 1)[1].split('hpcups_LDADD', 1)[0]
        files = sorted(set(re.findall(r'[\w/.-]+\.(?:cpp|c)\b', block)))
        objects = []
        with (OUTPUT / 'compile.log').open('w') as log:
            for i, name in enumerate(files):
                print(f'[{i+1}/{len(files)}] {name}', flush=True)
                obj = work / (name.replace('/', '_').replace('.', '_') + '.o')
                flags = ['clang++', '-std=c++11', '-include', 'common/utils.h'] if name.endswith('.cpp') else ['clang', '-DCONFDIR="/etc/hp"']
                run(flags + common + ['-c', name, '-o', obj], cwd=src, stdout=log, stderr=log)
                objects.append(obj)
            binary = OUTPUT / 'hpcups'
            run(['clang++', '-arch', 'x86_64', '-isysroot', sdk, '-o', binary, *objects,
                 jpeg / 'lib/libjpeg.a', '-lcups', '-lcupsimage', '-lz'], cwd=src, stdout=log, stderr=log)
        run(['codesign', '--force', '--sign', '-', binary])
        ppd = gzip.decompress((src / 'ppd/hpcups/hp-deskjet_2300_series.ppd.gz').read_bytes()).decode()
        old = '*cupsFilter: "application/vnd.cups-raster 0 hpcups"'
        assert old in ppd
        ppd = ppd.replace(old, '*cupsFilter: "application/vnd.cups-raster 0 /Library/Printers/hplip-local/hpcups"')
        (OUTPUT / 'HP-DeskJet-2376.ppd').write_text(ppd)
        (OUTPUT / 'binary.sha256').write_text(hashlib.sha256(binary.read_bytes()).hexdigest() + '\n')
        run(['file', binary])
        run(['otool', '-L', binary])
        names = ['hpcups', 'HP-DeskJet-2376.ppd', 'test-colors.pdf']
        (OUTPUT / 'install.sha256').write_text(''.join(hashlib.sha256((OUTPUT / n).read_bytes()).hexdigest() + '  ' + n + '\n' for n in names))
        print('Built from HP-signed sources. Nothing installed:', OUTPUT)


if __name__ == '__main__':
    main()
