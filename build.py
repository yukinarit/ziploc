#!/usr/bin/env python

from __future__ import print_function

import logging
import os
import sys
import traceback
import tempfile

logging.basicConfig(level=logging.DEBUG)

command = '''
set -x
pushd {tmpdir}
mkdir -p {name}/deps
{pip} download -r {requirements} -d {name}/deps

{python} -c '
import sys
sys.path.append("{basedir}")
import build
build.make_new_requirements("{requirements}",
                            "{name}/deps/requirements.txt")
'

cp {basedir}/installer.py {name}/__main__.py
cd {name}
zip -r ../{name}.pyz __main__.py deps
cd ..
popd
cp {tmpdir}/{name}.pyz .
'''

basedir = os.path.dirname(os.path.abspath(__file__))


def make_new_requirements(src, dst, recursive=False):
    dir = os.path.dirname(src)
    if not recursive:
        try:
            os.remove(dst)
        except:
            pass

    lines = []
    with open(src) as f:
        for line in f:
            if line.startswith('-r'):
                child = os.path.join(dir, line[3:])
                make_new_requirements(child, dst, recursive=True)
            else:
                lines.append(line)
    with open(dst, 'a') as f:
        f.writelines(lines)


def get_pip():
    python = sys.executable
    bindir = os.path.dirname(python)
    version = os.path.basename(python)[6:]
    pip = os.path.join(bindir, 'pip' + version)
    return pip


def main():
    tmpdir = tempfile.mkdtemp(dir='/tmp/')
    python = sys.executable
    pip = get_pip()
    name = sys.argv[1]
    requirements = os.path.abspath(os.path.expanduser(sys.argv[2]))
    logging.debug('tmpdir {}'.format(tmpdir))
    logging.debug('python {}'.format(python))
    logging.debug('pip {}'.format(pip))
    logging.debug('name {}'.format(name))
    logging.debug('requirements {}'.format(requirements))
    c = command.format(basedir=basedir, tmpdir=tmpdir, name=name, pip=pip,
                       requirements=requirements, python=sys.executable)
    os.system(c)


if __name__ == '__main__':
    sys.exit(main())
