#!/usr/bin/env python

import argparse
import re
import sys
import apt_pkg
from prometheus_client import core, Gauge
from prometheus_client import write_to_textfile, generate_latest


apt_package = Gauge(
    'apt_package',
    'apt package installed.',
    ['name', 'version']
)


def main(args):
    package_re = re.compile(args.regex)
    apt_pkg.init()
    cache = apt_pkg.Cache()
    for package in cache.packages:
        if package.current_ver:
            if package_re.search(package.name):
                apt_package.labels(package.name, package.current_ver.ver_str).set(True)
    if args.promfile:
        write_to_textfile(args.promfile, core.REGISTRY)
    else:
        print generate_latest(core.REGISTRY)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prometheus check apt packages.')
    parser.add_argument('--promfile')
    parser.add_argument('--regex', default='.*')
    main(parser.parse_args())
