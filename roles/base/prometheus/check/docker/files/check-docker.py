#!/usr/bin/env python

import argparse
from prometheus_client import core
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest
from prometheus_client import Counter
from prometheus_client.exposition import BaseHTTPRequestHandler, HTTPServer


CHECK_DOCKER_DUPLICATED_MAC_ADDRESS = Gauge(
    'check_docker_duplicated_mac_address',
    'Number of duplicated mac address',
)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Iptables Prometheus exporter.'
    )
    parser.add_argument(
        '--address', metavar='IP', type=str, default='',
        help='Listening address, default: all'
    )
    parser.add_argument(
        '--port', metavar='PORT', type=int, default=9119,
        help='Listening port, default: 9119'
    )
    parser.add_argument(
        '--tables', metavar='TABLE', type=str, nargs='+',
        choices=TABLE_CHOICES, default=DEFAULT_TABLE_CHOICES,
        help='List of tables, default: %s' % ', '.join(DEFAULT_TABLE_CHOICES)
    )
    parser.add_argument(
        '--dump-data', action='store_true', default=False,
        help='Prints collected data and exits'
    )
    args = parser.parse_args()

    # Test mode
    if args.dump_data:
        dump_data(args.tables)
        exit(0)

    # Start http server
    httpd = HTTPServer((args.address, args.port), MetricsHandler)
    httpd.RequestHandlerClass.tables = args.tables
    httpd.serve_forever()
