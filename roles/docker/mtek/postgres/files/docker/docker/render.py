#!/usr/bin/env python

import argparse
import sys
from jinja2 import Template
from data import data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='render template.')
    parser.add_argument(
        '--template',
        metavar='TEMPLATE',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    parser.add_argument(
        '--outfile',
        metavar='FILE',
        type=argparse.FileType('w'),
        default=sys.stdout
    )

    kwargs = vars(parser.parse_args())

    template = Template(kwargs['template'].read())
    kwargs['outfile'].write(template.render(data))
