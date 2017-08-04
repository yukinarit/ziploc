#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import tempfile

basedir = os.path.dirname(os.path.abspath(__file__))

command = '''
bash -c "
set -x
pushd {dest}
cp -rf {archive} .
unzip {name}
{pip} install -r deps/requirements.txt --no-index --find-links file://{dest}/deps/
popd
rm -r {dest}
"
'''


def get_pip():
    python = sys.executable
    bindir = os.path.dirname(python)
    version = os.path.basename(python)[6:]
    pip = os.path.join(bindir, 'pip' + version)
    return pip


def main():
    tmpdir = tempfile.mkdtemp(dir='/tmp/')
    pyz = os.path.abspath(os.path.dirname(__file__))
    name = os.path.basename(pyz)
    pip = get_pip()
    print('pyz {}'.format(pyz))
    print('tmpdir {}'.format(tmpdir))
    print('name {}'.format(name))
    print('pip {}'.format(pip))

    c = command.format(archive=pyz, name=name, dest=tmpdir, pip=pip)
    os.system(c)


if __name__ == '__main__':
    sys.exit(main())
