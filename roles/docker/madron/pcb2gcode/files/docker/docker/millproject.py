#!/usr/bin/env python

import argparse
import sys
from jinja2 import Template

TEMPLATE_FILE = '/docker/millproject.j2'
#TEMPLATE_FILE = '/Users/max/dev/anslib/roles/docker/madron/pcb2gcode/files/docker/docker/millproject.j2'
DEFAULT_OUTPUT = '/data/millproject'
#DEFAULT_OUTPUT = './millproject'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='render template.')
    parser.add_argument(
        '--creator',
        metavar='PROGRAM',
        choices=['target3001'],
        default='target3001',
    )
    parser.add_argument(
        '--base-name',
        metavar='BASE_NAME',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--outfile',
        metavar='FILE',
        type=argparse.FileType('w'),
        default=DEFAULT_OUTPUT,
    )

    kwargs = vars(parser.parse_args())
    print kwargs

    template = Template(open(TEMPLATE_FILE, 'r').read())
    kwargs['outfile'].write(template.render(kwargs))
