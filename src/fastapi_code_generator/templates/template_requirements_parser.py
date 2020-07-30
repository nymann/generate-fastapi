#!/usr/bin/env python3

import configparser
import sys

cfg = configparser.ConfigParser()
cfg.read('setup.cfg')

opts = cfg['options']

switch = {
    'install': 'install_requires',
    'test': 'tests_require',
    'setup': 'setup_requires'
}

rtn = []
pip_opts = [
    '--extra-index-url https://software.siemens.dk/pypi/',
    '--trusted-host software.siemens.dk'
]

for req in [opts[switch[arg]].strip() for arg in sys.argv[1:]]:
    rtn.extend(req.split('\n'))

pip_opts.extend(set(rtn))

print('\n'.join(pip_opts))
