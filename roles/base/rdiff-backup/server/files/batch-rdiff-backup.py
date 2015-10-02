#!/usr/bin/env python

import argparse
import logging
import os
import signal
import sys
import paramiko
import rdiff_backup.Main
import tempfile
import time
from contextlib import contextmanager
from StringIO import StringIO

BACKUP_BASE = '/var/backups'
LOG_DIR = '/var/log'
LOG_PREFIX = 'rdiff-backup'
DEFAULT_USER = 'root'
DEFAULT_PORT = 22

METRIC = dict(
    start_time=dict(
        type='gauge',
        help='Backup start time, in unixtime.',
    ),
    end_time=dict(
        type='gauge',
        help='Backup end time, in unixtime.',
    ),
    elapsed_seconds=dict(
        type='gauge',
        help='Total backup time, in seconds.',
    ),
    success=dict(
        type='gauge',
        help='Backup succedeed: 1 -> success - 0 -> failure.',
    ),
    command_start_time=dict(
        type='gauge',
        help='Pre execute command start time, in unixtime.',
    ),
    command_end_time=dict(
        type='gauge',
        help='Pre execute command end time, in unixtime.',
    ),
    command_elapsed_seconds=dict(
        type='gauge',
        help='Pre execute command time, in seconds.',
    ),
    command_success=dict(
        type='gauge',
        help='Pre execute command succedeed: 1 -> success - 0 -> failure.',
    ),
    transfer_start_time=dict(
        type='gauge',
        help='Transfer start time, in unixtime.',
    ),
    transfer_end_time=dict(
        type='gauge',
        help='Transfer end time, in unixtime.',
    ),
    transfer_elapsed_seconds=dict(
        type='gauge',
        help='Transfer time, in seconds.',
    ),
    transfer_success=dict(
        type='gauge',
        help='Transfer succedeed: 1 -> success - 0 -> failure.',
    ),
    source_size_bytes=dict(
        type='gauge',
        help='Source size, in bytes.',
    ),
    destination_size_change_bytes=dict(
        type='gauge',
        help='data transfered, in bytes',
    ),
    transfer_rate_bps=dict(
        type='gauge',
        help='Transfer rate, in bit per second.',
    ),
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


class PrometheusTextfile(object):
    def __init__(self, name, directory=None, prefix='rdiff_backup', group=None):
        self.name = name
        self.outfile = None
        if directory:
            self.outfile = os.path.join(directory, 'rdiff-backup-%s.prom' % name)
            if group:
                self.outfile = os.path.join(directory, 'rdiff-backup-%s-%s.prom' % (group, name))
        self.prefix = prefix
        self.labels = [('name', self.name)]
        if group:
            self.labels.append(('rdiff_group', group))
        self.rows = []

    def add(self, metric, labels=[], value=0):
        metric_name = '%s_%s' % (self.prefix, metric)
        # HELP node_boot_time Node boot time, in unixtime.
        self.rows.append('# HELP %s %s' % (metric_name, METRIC[metric]['help']))
        # TYPE node_boot_time gauge
        self.rows.append('# TYPE %s %s' % (metric_name, METRIC[metric]['type']))
        # value
        labels = self.labels + labels
        string_labels = ['%s="%s"' % (x[0], x[1]) for x in labels]
        metric_name = '%s{%s}' % (metric_name, ','.join(string_labels))
        self.rows.append('%s %s' % (metric_name, value))

    def write(self):
        if self.outfile:
            path = os.path.dirname(self.outfile)
            f = tempfile.NamedTemporaryFile(dir=path, delete=False)
            f.write('\n'.join(self.rows))
            f.write('\n')
            f.close()
            os.rename(f.name, self.outfile)


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


def remote_command(logger, ssh_client, command, no_errors=[], timeout=None):
    logger.info("Executing remote command: '%s'" % command)
    if timeout:
        try:
            with time_limit(timeout):
                stdin, stdout, stderr = ssh_client.exec_command(command)
                finished = stdout.channel.exit_status_ready()
                while not finished:
                    finished = stdout.channel.exit_status_ready()
                rc = stdout.channel.recv_exit_status()
        except TimeoutException:
            logger.error('Command timeout excedeed (%d seconds).' % timeout)
            return 1, '', ''
    else:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        finished = stdout.channel.exit_status_ready()
        while not finished:
            finished = stdout.channel.exit_status_ready()
        rc = stdout.channel.recv_exit_status()
    stdout_lines = [l.rstrip() for l in stdout.readlines()]
    stderr_lines = []
    for line in [l.rstrip() for l in stderr.readlines()]:
        is_error = True
        for text in no_errors:
            if line.startswith(text):
                is_error = False
        if is_error:
            stderr_lines.append(line)
        else:
            stdout_lines.append(line)
    for line in stdout_lines:
        logger.info(line)
    for line in stderr_lines:
        logger.error(line)
    rc_message = 'Return code: %d' % rc
    if rc == 0:
        logger.info(rc_message)
    else:
        logger.error(rc_message)
    return rc, stdout.read(), stderr.read()


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
    rc = 1 if stderr_lines else 0
    return rc, stdout_lines, stderr_lines


def run(**kwargs):
    kwargs['name'] = kwargs['name'] or kwargs['host']
    kwargs['backup_dir'] = kwargs['backup_dir'] or os.path.join(kwargs['backup_base'], kwargs['name'])
    logger = get_logger(kwargs['sysout'], kwargs['name'], kwargs['log_prefix'])
    logger.info('=' * 50)
    logger.info('Backup started.')
    logger.debug(kwargs)
    kwargs['logger'] = logger
    prom = PrometheusTextfile(kwargs['name'], directory=kwargs['prometheus_dir'], group=kwargs['prometheus_group'])
    kwargs['prom'] = prom
    host = kwargs['host']
    port = kwargs['port']
    user = kwargs['user']
    command_timeout = kwargs['command_timeout']
    start_time = float(time.time())
    prom.add('start_time', value=start_time)
    prom.write()
    pre_execute_commands = kwargs['pre_execute_commands']
    no_errors = kwargs['no_errors']
    failure = False
    if host == 'localhost' and pre_execute_commands:
        logger.error('pre_execute_commands not supported on localhost')
        return
    try:
        #Connection check and pre-exececute-commands
        if not host == 'localhost':
            ssh_client = get_ssh_client(host, port, user)
            for command in pre_execute_commands:
                labels = [('command', command.replace('"', "'"))]
                command_start_time = float(time.time())
                prom.add('command_start_time', labels=labels, value=command_start_time)
                prom.write()
                rc, out, err = remote_command(logger, ssh_client, command, no_errors=no_errors, timeout=command_timeout)
                value = 1
                if rc:
                    failure = True
                    value = 0
                command_end_time = float(time.time())
                prom.add('command_end_time', labels=labels, value=command_end_time)
                command_elapsed_seconds = command_end_time - command_start_time
                prom.add('command_elapsed_seconds', labels=labels, value=command_elapsed_seconds)
                prom.add('command_success', labels=labels, value=value)
                prom.write()
            ssh_client.close()
        # Backup
        transfer_start_time = float(time.time())
        rc, stdout_lines, stderr_lines = backup(**kwargs)
        value = 1
        if rc:
            failure = True
            value = 0
            prom.add('transfer_start_time', value=transfer_start_time)
            transfer_end_time = float(time.time())
            prom.add('transfer_end_time', value=transfer_end_time)
            transfer_elapsed_seconds = transfer_end_time - transfer_start_time
            prom.add('transfer_elapsed_seconds', labels=labels, value=transfer_elapsed_seconds)
        else:
            stats = parse_statistics(stdout_lines)
            for k, v in stats.iteritems():
                prom.add(k, value=v)
        prom.add('transfer_success', value=value)
        prom.write()
        # Check
        rc = check_backup(**kwargs)
        if rc:
            failure = True
        # Clean
        rc, stdout_lines, stderr_lines = clean_backup(**kwargs)
        if rc:
            failure = True
    except:
        logger.exception('Unexpected error')
        failure = True
    end_time = float(time.time())
    prom.add('end_time', value=end_time)
    elapsed_seconds = end_time - start_time
    prom.add('elapsed_seconds', value=elapsed_seconds)
    value = 1
    if failure:
        value = 0
    prom.add('success', value=value)
    prom.write()
    logger.info('Backup finished.')


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
    user = kwargs['user']
    includes = kwargs['includes']
    excludes = kwargs['excludes']
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
    args.extend(['--exclude', '/'])
    if host == 'localhost':
        args.append('/')
    else:
        args.append('--remote-schema')
        args.append('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -C -p %d ' % port + ' %s rdiff-backup --server')
        args.append('%s@%s::/' % (user, host))
    args.append(backup_dir)
    logger.info('File transfer started.')
    return rdiff_backup_command(logger, args, timeout=timeout)


def check_backup(**kwargs):
    logger = kwargs['logger']
    includes = kwargs['includes']
    backup_dir = kwargs['backup_dir']
    rc = 0
    for remote_path in includes:
        path = os.path.join(backup_dir, remote_path.lstrip('/'))
        logger.info("Checking path: '%s'" % path)
        if not os.path.exists(path):
            rc = 1
            logger.error("Path '%s' does not exist on remote host" % remote_path)
    return rc


def clean_backup(**kwargs):
    logger = kwargs['logger']
    backup_dir = kwargs['backup_dir']
    days = kwargs['retain_days']
    if not days:
        logger.info('retain-days parameter not supplied: not removing old backups.')
        return 0, [], []
    logger.info('Removing backups older than %d days.' % days)
    args = []
    args.append('--force')
    args.append('--remove-older-than')
    args.append('%dD' % days)
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
    parser.add_argument('--includes', metavar='PATH', type=str, nargs='+',
                        required=True, help='Paths to backup')
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
                        help='Commands to execute on remote host')
    parser.add_argument('--command-timeout', metavar='SECONDS',
                        type=int, default=None,
                        help='Timeout for pre execute command')
    parser.add_argument('--transfer-timeout', metavar='SECONDS',
                        type=int, default=None,
                        help='Timeout for transfer')
    parser.add_argument('--no-errors', metavar='TEXT',
                        type=str, nargs='+', default=[],
                        help='Commands to execute on remote host')
    parser.add_argument('--prometheus-dir', metavar='DIR', type=str, default='',
                        help='Prometheus textfile collector directory')
    parser.add_argument('--prometheus-group', metavar='GROUP', type=str, default='',
                        help='Prometheus rdiff_group label')
    parser.add_argument('--retain-days', metavar='DAYS', type=int,
                        help='Remove backups older than specified days')
    parser.add_argument('--sysout', action='store_true', default=False,
                        help='Log to sysout')

    kwargs = vars(parser.parse_args())
    run(**kwargs)
