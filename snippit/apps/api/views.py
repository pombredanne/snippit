#!/usr/bin/env python
from __future__ import with_statement
import os
import re
import shutil
import subprocess
import sys
import tempfile

select_codes = ["E111", "E125", "E203", "E261", "E262", "E301", "E302", "E303",
                "E502", "E701", "E711", "W291", "W293"]


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def hilite(text, status, bold=False):
    attrs = []
    colors = {
        'green': '32', 'red': '31', 'yellow': '33'
    }
    if not sys.stdout.isatty():
        return text
    attrs.append(colors.get(status, 'red'))
    attrs.append('1') if bold else ''
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attrs), text)


def exists(cmd):
    devnull = open(os.devnull, 'w')
    params = {'stdout': devnull, 'stderr': devnull, }
    query = 'which %s' % cmd
    code = subprocess.call(query.split(), **params)
    if code != 0:
        print hilite('not installed %(command)s, pip install %(command)s' % {
            'command': cmd}, 'yellow', True)
        sys.exit(1)


def main():
    exists('pep8')
    exists('pyflakes')
    modified = re.compile('^[AM]+\s+(?P<name>.*\.py)', re.MULTILINE)
    files = system('git', 'status', '--porcelain')
    files = modified.findall(files)

    tempdir = tempfile.mkdtemp()
    for name in files:
        filename = os.path.join(tempdir, name)
        filepath = os.path.dirname(filename)

        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with file(filename, 'w') as f:
            system('git', 'show', ':' + name, stdout=f)

    pep8_output = system('pep8', '--select', ','.join(select_codes), '.',
                         cwd=tempdir)
    pyflakes_output = system('pyflakes', '.', cwd=tempdir)
    shutil.rmtree(tempdir)
    if pep8_output:
        print hilite('PEP8 style violations have been detected. '
                     'Please fix them\n or force the commit with '
                     '"git commit --no-verify".\n', 'red', True)
        print hilite(pep8_output, 'red'),
        sys.exit(1)
    if pyflakes_output:
        print hilite('The following Python flakes were found. '
                     'Please fix them or  force the commit with '
                     '"git commit --no-verify" \n', 'red', True)
        print hilite(pyflakes_output, 'red')
        sys.exit(1)

if __name__ == '__main__':
    main()
