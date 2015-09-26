#!/usr/bin/env python

import os
import re
import subprocess
import sys
import unittest
from ConfigParser import SafeConfigParser

PATH = {
    'gnome-terminal': 'gnome-terminal',
    'terminator': 'terminator',
    'putty': 'putty',
}
OPTIONS = {
    'gnome-terminal': '--tab --active',
    'terminator': '--new-tab',
    'putty': '',
}


def parse_url(url):
    regex = r'^ssh://((?P<user>.+)@)?(?P<host>[^:]+)(:(?P<port>\d+))?$'
    match = re.match(regex, url)
    if not match:
        raise RuntimeError()
    params = match.groupdict()
    if params['port']:
        params['port'] = int(params['port'])
    return params


def get_config(config_file, terminal=None):
    config = SafeConfigParser(
        defaults=dict(terminal='gnome-terminal', path=None, options='')
    )
    config.read(config_file)
    if not terminal:
        terminal = config.get('DEFAULT', 'terminal')
    path = config.get('DEFAULT', 'path')
    if not path:
        path = PATH[terminal]
    options = config.get('DEFAULT', 'options')
    if not options:
        options = OPTIONS[terminal]
    return dict(
        terminal=terminal,
        path=path,
        options=options,
    )


def get_ssh_command(parameters):
    user = ''
    if parameters['user']:
        user = '%s@' % parameters['user']
    port = ''
    if parameters['port']:
        port = ' -p %d' % parameters['port']
    return 'ssh %s%s%s' % (user, parameters['host'], port)


def get_command_args(config, parameters):
    args = [config['path']]
    if config['options']:
        args += config['options'].split()
    args += ['--title', '"%s"' % parameters['host']]
    if config['terminal'] in ('gnome-terminal', 'terminator'):
        args += [
            '--command', '"%s"' % get_ssh_command(parameters),
        ]
    if config['terminal'] == 'putty':
        if parameters['user']:
            args += ['-l', parameters['user']]
        if parameters['port']:
            args += ['-P', str(parameters['port'])]
        args.append(parameters['host'])
    return args


class TestParseUrl(unittest.TestCase):
    def test_wrong_protocol(self):
        with self.assertRaises(RuntimeError):
            parse_url('scp://root@www.example.com')

    def test_wrong_syntax(self):
        with self.assertRaises(RuntimeError):
            parse_url('ssh:/www.example.com')
        with self.assertRaises(RuntimeError):
            parse_url('ssh//www.example.com')

    def test_domain(self):
        self.assertEqual(
            parse_url('ssh://www.example.com'),
            dict(user=None, host='www.example.com', port=None)
        )

    def test_user_domain(self):
        self.assertEqual(
            parse_url('ssh://root@www.example.com'),
            dict(user='root', host='www.example.com', port=None)
        )

    def test_user_domain_port(self):
        self.assertEqual(
            parse_url('ssh://root@www.example.com:3022'),
            dict(user='root', host='www.example.com', port=3022)
        )

    def test_domain_port(self):
        self.assertEqual(
            parse_url('ssh://www.example.com:3022'),
            dict(user=None, host='www.example.com', port=3022)
        )

    def test_ip(self):
        self.assertEqual(
            parse_url('ssh://192.168.1.1'),
            dict(user=None, host='192.168.1.1', port=None)
        )

    def test_user_ip(self):
        self.assertEqual(
            parse_url('ssh://root@192.168.1.1'),
            dict(user='root', host='192.168.1.1', port=None)
        )

    def test_user_ip_port(self):
        self.assertEqual(
            parse_url('ssh://root@192.168.1.1:3022'),
            dict(user='root', host='192.168.1.1', port=3022)
        )

    def test_ip_port(self):
        self.assertEqual(
            parse_url('ssh://192.168.1.1:3022'),
            dict(user=None, host='192.168.1.1', port=3022)
        )


class TestGetCommandArgs(unittest.TestCase):
    def test_gnome_terminal_domain(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='gnome-terminal', path='gnome-terminal',
                     options='--tab --active'),
                dict(user=None, host='www.example.com', port=None),
            ),
            ['gnome-terminal', '--tab', '--active',
             '--title', '"www.example.com"',
             '--command', '"ssh www.example.com"']
        )

    def test_gnome_terminal_user_domain(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='gnome-terminal', path='gnome-terminal',
                     options='--tab'),
                dict(user='root', host='www.example.com', port=None)
            ),
            ['gnome-terminal', '--tab',
             '--title', '"www.example.com"',
             '--command', '"ssh root@www.example.com"']
        )

    def test_gnome_terminal_user_domain_port(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='gnome-terminal', path='gnome-terminal',
                     options=''),
                dict(user='root', host='www.example.com', port=3022)
            ),
            ['gnome-terminal', '--title', '"www.example.com"',
             '--command', '"ssh root@www.example.com -p 3022"']
        )

    def test_terminator_domain(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='terminator', path='terminator',
                     options='--new-tab --maximise'),
                dict(user=None, host='www.example.com', port=None),
            ),
            ['terminator', '--new-tab', '--maximise',
             '--title', '"www.example.com"',
             '--command', '"ssh www.example.com"']
        )

    def test_terminator_user_domain(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='terminator', path='terminator',
                     options='--new-tab'),
                dict(user='root', host='www.example.com', port=None)
            ),
            ['terminator', '--new-tab', '--title', '"www.example.com"',
             '--command', '"ssh root@www.example.com"']
        )

    def test_terminator_user_domain_port(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='terminator', path='/usr/bin/terminator',
                     options=''),
                dict(user='root', host='www.example.com', port=3022)
            ),
            ['/usr/bin/terminator', '--title', '"www.example.com"',
             '--command', '"ssh root@www.example.com -p 3022"']
        )

    def test_putty_domain(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='putty', path='putty',
                     options='-i ~/.ssh/putty_rsa'),
                dict(user=None, host='www.example.com', port=None),
            ),
            ['putty', '-i', '~/.ssh/putty_rsa',
             '--title', '"www.example.com"', 'www.example.com']
        )

    def test_putty_user_domain(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='putty', path='putty', options=''),
                dict(user='root', host='www.example.com', port=None)
            ),
            ['putty', '--title', '"www.example.com"',
             '-l', 'root', 'www.example.com']
        )

    def test_putty_user_domain_port(self):
        self.assertEqual(
            get_command_args(
                dict(terminal='putty', path='putty', options=''),
                dict(user='root', host='www.example.com', port=3022)
            ),
            ['putty', '--title', '"www.example.com"',
             '-l', 'root', '-P', '3022', 'www.example.com']
        )


if __name__ == '__main__':
    from optparse import OptionParser
    default_config = os.path.join('~', '.wrapper-ssh')
    usage = "usage: %prog [options] url"
    parser = OptionParser(usage)
    parser.add_option('-c', '--config', dest='config',
                      help='Configuration file. Default: %s' % default_config,
                      metavar='FILE', default=default_config)
    parser.add_option('-t', '--terminal', dest='terminal',
                      help='Terminal client. choices: gnome-terminal, terminator, putty',
                      metavar='TERM')
    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False,
                      help='Verbose output')
    parser.add_option('--run-tests',
                      action='store_true', dest='tests', default=False,
                      help='Run unit tests and exit')

    (options, args) = parser.parse_args()

    if options.tests:
        sys.argv = sys.argv[0:1]
        exit(unittest.main(argv=None))

    if len(args) == 0:
        parser.print_usage()
        exit(1)

    parameters = parse_url(args[0])
    config = get_config(options.config, terminal=options.terminal)
    command_args = get_command_args(config, parameters)
    if options.verbose:
        print ' '.join(command_args)
    exit(subprocess.call(' '.join(command_args), shell=True))
