#!/usr/bin/env python

import argparse
from docker import Client
from prometheus_client import core
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest
from prometheus_client import Gauge
from prometheus_client.exposition import BaseHTTPRequestHandler, HTTPServer


CHECK_DOCKER_DUPLICATED_MAC_ADDRESS = Gauge(
    'check_docker_duplicated_mac_address',
    'Number of duplicated mac address',
)
CHECK_DOCKER_DUPLICATED_IP_ADDRESS = Gauge(
    'check_docker_duplicated_ip_address',
    'Number of duplicated ip address',
)
DEFAULT_DOCKER_BASE_URL = 'unix://var/run/docker.sock'
DEFAULT_PORT = 9120


class MetricsHandler(BaseHTTPRequestHandler):
    docker_base_url = DEFAULT_DOCKER_BASE_URL

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', CONTENT_TYPE_LATEST)
        self.end_headers()
        collect_metrics(self.docker_base_url)
        self.wfile.write(generate_latest(core.REGISTRY))

    def log_message(self, format, *args):
        return


def collect_metrics(docker_base_url):
    cli = Client(base_url=docker_base_url)
    containers = cli.containers(all=True)
    mac_dict = dict()
    ip_dict = dict()
    for container in containers:
        id = container['Id']
        name = container['Names'][0]
        config = cli.inspect_container(id)
        mac = config['NetworkSettings']['MacAddress']
        if mac:
            mac_dict[mac] = mac_dict.get(mac, 0) + 1
        ip = config['NetworkSettings']['IPAddress']
        if ip:
            ip_dict[mac] = ip_dict.get(ip, 0) + 1
    duplicated_mac_address = 0
    for mac, count in mac_dict.iteritems():
        if count > 1:
            duplicated_mac_address += 1
    duplicated_ip_address = 0
    for ip, count in ip_dict.iteritems():
        if count > 1:
            duplicated_ip_address += 1
    CHECK_DOCKER_DUPLICATED_MAC_ADDRESS.set(duplicated_mac_address)
    CHECK_DOCKER_DUPLICATED_IP_ADDRESS.set(duplicated_ip_address)


def dump_data(docker_base_url):
    collect_metrics(docker_base_url)
    print(generate_latest(core.REGISTRY))


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Check Docker Prometheus exporter.'
    )
    parser.add_argument(
        '--address', metavar='IP', type=str, default='',
        help='Listening address, default: all'
    )
    parser.add_argument(
        '--port', metavar='PORT', type=int, default=DEFAULT_PORT,
        help='Listening port, default: %d' % DEFAULT_PORT
    )
    parser.add_argument(
        '--docker-base-url', metavar='URL', type=str,
        default=DEFAULT_DOCKER_BASE_URL,
        help='Docker base url - default: %s' % DEFAULT_DOCKER_BASE_URL
    )
    parser.add_argument(
        '--dump-data', action='store_true', default=False,
        help='Prints collected data and exits'
    )
    args = parser.parse_args()

    # Test mode
    if args.dump_data:
        dump_data(args.docker_base_url)
        exit(0)

    # Start http server
    httpd = HTTPServer((args.address, args.port), MetricsHandler)
    httpd.RequestHandlerClass.docker_base_url = args.docker_base_url
    httpd.serve_forever()


if __name__ == '__main__':
    main()
