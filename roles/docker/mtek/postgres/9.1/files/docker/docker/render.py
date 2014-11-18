#!/usr/bin/env python

import argparse
import os
import sys
from jinja2 import Template
from netaddr import IPNetwork


allowed_networks = os.getenv('allowed_networks', [])
if allowed_networks:
    allowed_networks = allowed_networks.replace(' ', '')
    allowed_networks = allowed_networks.split(',')
    allowed_networks = [IPNetwork(n) for n in allowed_networks]
allowed_replication_networks = os.getenv('allowed_replication_networks', [])
if allowed_replication_networks:
    allowed_replication_networks = allowed_replication_networks.replace(' ', '')
    allowed_replication_networks = allowed_replication_networks.split(',')
    allowed_replication_networks = [IPNetwork(n) for n in allowed_replication_networks]


data = dict(
    wal_keep_segments=os.getenv('wal_keep_segments', 0),
    master_server=os.getenv('master_server', None),
    allowed_networks=allowed_networks,
    allowed_replication_networks=allowed_replication_networks,
)


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
