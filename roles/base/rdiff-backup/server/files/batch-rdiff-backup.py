#!/usr/bin/env python

import argparse
import logging
import os
import signal
import sys
import paramiko
import platform
import rdiff_backup.Main
from contextlib import contextmanager
from StringIO import StringIO
from prometheus_client import REGISTRY, CollectorRegistry
from prometheus_client import Gauge
from prometheus_client import pushadd_to_gateway

BACKUP_BASE = '/var/backups'
LOG_DIR = '/var/log'
LOG_PREFIX = 'rdiff-backup'
DEFAULT_USER = 'root'
DEFAULT_PORT = 22
DEFAULT_TIMEOUT = 86400
BUFF_SIZE = 1024
LABELS = ['rdiff_group', 'name']

success_registry = CollectorRegistry()

# Time metrics
rdiff_backup_seconds = Gauge(
    'rdiff_backup_seconds',
    'rdiff-backup time, in seconds.',
)
rdiff_backup_command_seconds = Gauge(
    'rdiff_backup_command_seconds',
    'Commands time, in seconds.',
)
rdiff_backup_transfer_seconds = Gauge(
    'rdiff_backup_transfer_seconds',
    'Transfer time, in seconds.',
)
# Success metrics
rdiff_backup_command_success = Gauge(
    'rdiff_backup_command_success',
    'Command succedeed: 1 -> success - 0 -> failure.',
)
rdiff_backup_transfer_success = Gauge(
    'rdiff_backup_transfer_success',
    'Transfer succedeed: 1 -> success - 0 -> failure.',
)
rdiff_backup_success = Gauge(
    'rdiff_backup_success',
    'Backup succedeed: 1 -> success - 0 -> failure.',
)
rdiff_backup_success_time = Gauge(
    'rdiff_backup_success_time',
    'Backup success time, in unixtime.',
    registry=success_registry,
)
# Statistics metrics
rdiff_backup_source_size_bytes = Gauge(
    'rdiff_backup_source_size_bytes',
    'Source size, in bytes.',
)
rdiff_backup_destination_size_change_bytes = Gauge(
    'rdiff_backup_destination_size_change_bytes',
    'data transfered, in bytes',
)
rdiff_backup_transfer_rate_bps = Gauge(
    'rdiff_backup_transfer_rate_bps',
    'Transfer rate, in bit per second.',
)


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException('Timeout excedeed (%d seconds).' % seconds)
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def get_logger(sysout, host, log_prefix):
    logger = logging.getLogger('rdiff-backup')
    logger.setLevel(logging.DEBUG)
    formatter_string = '%(asctime)s ' + host + ' %(levelname)-5s %(message)s'
    if sysout:
        formatter = logging.Formatter(formatter_string, '%H:%M:%S')
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        formatter = logging.Formatter(formatter_string, '%Y-%m-%d %H:%M:%S')
        info_file = os.path.join(LOG_DIR, '%s-info.log' % log_prefix)
        info_handler = logging.FileHandler(info_file)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)
        error_file = os.path.join(LOG_DIR, '%s-error.log' % log_prefix)
        error_handler = logging.FileHandler(error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
    return logger


def get_ssh_client(host, port, user):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user)
    return client


def is_error(line, no_errors):
    is_error = True
    for text in no_errors:
        if line.startswith(text):
            is_error = False
    return is_error


def remote_command(logger, ssh_client, command, no_errors=[], timeout=DEFAULT_TIMEOUT):
    logger.info("Executing remote command: '%s'" % command)
    timeout = timeout or DEFAULT_TIMEOUT
    channel = ssh_client.get_transport().open_session()
    channel.exec_command(command)

    try:
        with time_limit(timeout):
            while not channel.exit_status_ready():
                if channel.recv_ready():
                    lines = channel.recv(BUFF_SIZE).strip()
                    for line in lines.splitlines():
                        logger.info(line)
                if channel.recv_stderr_ready():
                    lines = channel.recv_stderr(BUFF_SIZE).strip()
                    for line in lines.splitlines():
                        if is_error(line, no_errors):
                            logger.error(line)
                        else:
                            logger.info(line)
            rc = channel.recv_exit_status()
            # Need to gobble up any remaining output after program terminates...
            while channel.recv_ready():
                lines = channel.recv(BUFF_SIZE).strip()
                for line in lines.splitlines():
                    logger.info(line)
            while channel.recv_stderr_ready():
                lines = channel.recv_stderr(BUFF_SIZE).strip()
                for line in lines.splitlines():
                    if is_error(line, no_errors):
                        logger.error(line)
                    else:
                        logger.info(line)
    except TimeoutException:
        logger.error('Command timeout excedeed (%d seconds).' % timeout)
        return 1
    finally:
        channel.close()

    rc_message = 'Return code: %d' % rc
    if rc == 0:
        logger.info(rc_message)
    else:
        logger.error(rc_message)
    return rc


def rdiff_backup_command(logger, args, timeout=None):
    logger.debug('rdiff_backup_command arguments: %s' % args)
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    stdout = StringIO()
    stderr = StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    timed_out = False
    try:
        if timeout:
            with time_limit(timeout):
                rdiff_backup.Main.error_check_Main(args)
        else:
            rdiff_backup.Main.error_check_Main(args)
    except TimeoutException:
        timed_out = True
    except:
        pass
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        stdout.seek(0)
        stderr.seek(0)
        stdout_lines = [l.rstrip() for l in stdout.readlines()]
        stderr_lines = [l.rstrip() for l in stderr.readlines()]
        if timed_out:
            stderr_lines.append('Transfer timeout excedeed (%d seconds).' % timeout)
    for line in stdout_lines:
        logger.info(line)
    for line in stderr_lines:
        logger.error(line)
    success = not stderr_lines
    return success, stdout_lines, stderr_lines


def run(**kwargs):
    kwargs['name'] = kwargs['name'] or kwargs['host']
    kwargs['backup_dir'] = kwargs['backup_dir'] or os.path.join(kwargs['backup_base'], kwargs['name'])
    # Logger
    logger = get_logger(kwargs['sysout'], kwargs['name'], kwargs['log_prefix'])
    logger.info('=' * 50)
    logger.info('Backup started.')
    logger.debug(kwargs)
    kwargs['logger'] = logger
    # Pushgateway parameters
    pushgateway_kwargs = dict()
    if kwargs['prometheus_pushgateway_url']:
        grouping_key = dict(
            name=kwargs['name'],
            rdiff_instance=kwargs['prometheus_instance'],
        )
        if kwargs['prometheus_group']:
            grouping_key['rdiff_group'] = kwargs['prometheus_group']
        pushgateway_kwargs = dict(
            registry=REGISTRY,
            gateway=kwargs['prometheus_pushgateway_url'],
            job='rdiff-backup',
            grouping_key=grouping_key,
            timeout=kwargs['prometheus_pushgateway_timeout'],
        )
    kwargs['pushgateway_kwargs'] = pushgateway_kwargs
    # Backup
    try:
        success = run_backup(**kwargs)
    except:
        logger.exception('Unexpected error')
        success = False
    if pushgateway_kwargs:
        try:
            pushadd_to_gateway(**pushgateway_kwargs)
            if success:
                pushgateway_kwargs['registry'] = success_registry
                pushadd_to_gateway(**pushgateway_kwargs)
        except:
            logger.exception('Prometheus pushgateway error')
    logger.info('Backup finished.')


@rdiff_backup_seconds.time()
def run_backup(**kwargs):
    # Pre command
    pre_command_success = run_command('pre', **kwargs)
    rdiff_backup_command_success.set(pre_command_success)
    # Transfer
    transfer_success = run_transfer(**kwargs)
    rdiff_backup_transfer_success.set(transfer_success)
    # Post command
    command_success = run_command('post', **kwargs)
    command_success = command_success and pre_command_success
    rdiff_backup_command_success.set(command_success)
    # Backup
    success = command_success and transfer_success
    rdiff_backup_success.set(success)
    if success:
        rdiff_backup_success_time.set_to_current_time()
    return success


@rdiff_backup_command_seconds.time()
def run_command(type, **kwargs):
    logger = kwargs['logger']
    host = kwargs['host']
    port = kwargs['port']
    user = kwargs['user']
    command_timeout = kwargs['command_timeout']
    if type == 'pre':
        commands = kwargs['pre_execute_commands']
    else:
        commands = kwargs['post_execute_commands']
    no_errors = kwargs['no_errors']
    success = True
    if host == 'localhost' and commands:
        logger.error('execute_commands not supported on localhost')
        return False
    #Connection check and exececute commands
    if not host == 'localhost':
        ssh_client = get_ssh_client(host, port, user)
        for command in commands:
            rc = remote_command(logger, ssh_client, command, no_errors=no_errors, timeout=command_timeout)
            if rc:
                success = False
        ssh_client.close()
    return success


@rdiff_backup_transfer_seconds.time()
def run_transfer(**kwargs):
    success, stdout_lines, stderr_lines = backup(**kwargs)
    if success:
        stats = parse_statistics(stdout_lines)
        rdiff_backup_source_size_bytes.set(stats['source_size_bytes'])
        rdiff_backup_destination_size_change_bytes.set(stats['destination_size_change_bytes'])
        rdiff_backup_transfer_rate_bps.set(stats['transfer_rate_bps'])
    # Check
    if success:
        if not check_backup(**kwargs):
            success = False
    # Clean
    if success:
        if not clean_backup(**kwargs):
            success = False
    return success


def parse_statistics(lines):
    stats = dict()
    for line in lines:
        if line.startswith('StartTime'):
            stats['transfer_start_time'] = float(line.split(' ')[1])
        if line.startswith('EndTime'):
            stats['transfer_end_time'] = float(line.split(' ')[1])
        if line.startswith('ElapsedTime'):
            stats['transfer_elapsed_seconds'] = float(line.split(' ')[1])
        if line.startswith('SourceFileSize'):
            stats['source_size_bytes'] = int(line.split(' ')[1])
        if line.startswith('TotalDestinationSizeChange'):
            stats['destination_size_change_bytes'] = int(line.split(' ')[1])
    stats['transfer_rate_bps'] = stats['destination_size_change_bytes'] / stats['transfer_elapsed_seconds'] * 8
    return stats


def backup(**kwargs):
    logger = kwargs['logger']
    host = kwargs['host']
    port = kwargs['port']
    push = kwargs['push']
    user = kwargs['user']
    source = kwargs['source']
    if source:
        includes = []
        excludes = []
    else:
        includes = kwargs['includes']
        excludes = kwargs['excludes']
        source = '/'
    backup_dir = kwargs['backup_dir']
    timeout = kwargs['transfer_timeout']
    args = [
        '--create-full-path',
        '--print-statistics',
    ]
    for path in excludes:
        args.append('--exclude')
        args.append(path)
    for path in includes:
        args.append('--include')
        args.append(path)
    if includes:
        args.extend(['--exclude', '/'])
    if host == 'localhost':
        args.append(source)
        args.append(backup_dir)
    else:
        args.append('--remote-schema')
        args.append('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -C -p %d ' % port + ' %s rdiff-backup --server')
        if push:
            args.append(source)
            args.append('%s@%s::%s' % (user, host, backup_dir))
        else:
            args.append('%s@%s::%s' % (user, host, source))
            args.append(backup_dir)
    logger.info('File transfer started.')
    return rdiff_backup_command(logger, args, timeout=timeout)


def check_backup(**kwargs):
    logger = kwargs['logger']
    source = kwargs['source']
    if source:
        includes = [source]
    else:
        includes = kwargs['includes']
    backup_dir = kwargs['backup_dir']
    push = kwargs['push']
    success = True
    if not push:
        for remote_path in includes:
            path = os.path.join(backup_dir, remote_path.lstrip('/'))
            logger.info("Checking path: '%s'" % path)
            if not os.path.exists(path):
                success = False
                logger.error("Path '%s' does not exist on remote host" % remote_path)
    return success


def clean_backup(**kwargs):
    logger = kwargs['logger']
    backup_dir = kwargs['backup_dir']
    days = kwargs['retain_days']
    push = kwargs['push']
    host = kwargs['host']
    port = kwargs['port']
    user = kwargs['user']
    if not days:
        logger.info('retain-days parameter not supplied: not removing old backups.')
        return 0, [], []
    logger.info('Removing backups older than %d days.' % days)
    args = []
    args.append('--force')
    args.append('--remove-older-than')
    args.append('%dD' % days)
    if push:
        args.append('--remote-schema')
        args.append('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -C -p %d ' % port + ' %s rdiff-backup --server')
        args.append('%s@%s::%s' % (user, host, backup_dir))
    else:
        args.append('--remote-schema')
        args.append('')
        args.append(backup_dir)
    return rdiff_backup_command(logger, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='rdiff-backup.')
    parser.add_argument('--name', metavar='NAME', type=str, default='',
                        help='Name of host to backup')
    parser.add_argument('--host', metavar='HOSTNAME', type=str, required=True,
                        help='Host to backup')
    parser.add_argument('--port', metavar='PORT', type=int, default=DEFAULT_PORT,
                        help='Ssh port')
    parser.add_argument('--user', metavar='USER', type=str, default=DEFAULT_USER,
                        help='Ssh user')
    parser.add_argument('--push', default=False, action='store_true',
                        help='Push backup instead of pull.')
    parser.add_argument('--source', metavar='PATH', type=str, default='',
                        help='Path to backup')
    parser.add_argument('--includes', metavar='PATH', type=str, nargs='+',
                        default=[], help='Paths to backup')
    parser.add_argument('--excludes', metavar='PATH', type=str, nargs='+',
                        default=[], help='Paths to exclude from backup')
    parser.add_argument('--backup-base', metavar='DIR', type=str,
                        default=BACKUP_BASE, help='Backup base directory')
    parser.add_argument('--backup-dir', metavar='DIR', type=str, default='',
                        help='Backup directory (If not provided will be calculated with backup-base and name or host')
    parser.add_argument('--log-prefix', metavar='PREFIX', type=str,
                        default=LOG_PREFIX, help='Log file name prefix')
    parser.add_argument('--pre-execute-commands', metavar='COMMAND',
                        type=str, nargs='+', default=[],
                        help='Commands to execute on remote host before transfer')
    parser.add_argument('--post-execute-commands', metavar='COMMAND',
                        type=str, nargs='+', default=[],
                        help='Commands to execute on remote host after transfer')
    parser.add_argument('--command-timeout', metavar='SECONDS',
                        type=int, default=None,
                        help='Timeout for execute command')
    parser.add_argument('--transfer-timeout', metavar='SECONDS',
                        type=int, default=None,
                        help='Timeout for transfer')
    parser.add_argument('--no-errors', metavar='TEXT',
                        type=str, nargs='+', default=[],
                        help='Commands to execute on remote host')
    parser.add_argument('--prometheus-pushgateway-url', metavar='URL', type=str, default='',
                        help='Prometheus pushgateway url')
    parser.add_argument('--prometheus-pushgateway-timeout', metavar='SECONDS', type=int, default=5,
                        help='Prometheus pushgateway timeout (default: 5)')
    parser.add_argument('--prometheus-group', metavar='GROUP', type=str, default='',
                        help='Prometheus rdiff_group label')
    parser.add_argument('--prometheus-instance', metavar='HOST', type=str, default=platform.node(),
                        help='Prometheus rdiff_group label')
    parser.add_argument('--retain-days', metavar='DAYS', type=int,
                        help='Remove backups older than specified days')
    parser.add_argument('--sysout', action='store_true', default=False,
                        help='Log to sysout')

    kwargs = vars(parser.parse_args())
    run(**kwargs)
