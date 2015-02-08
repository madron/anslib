#!/usr/bin/env python3

from subprocess import check_output
from context import data


def get_vhost_list():
    vhost_list = check_output(["rabbitmqctl", "list_vhosts"]).splitlines()
    vhost_list = [i.decode("utf-8") for i in vhost_list]
    vhost_list.remove('Listing vhosts ...')
    return vhost_list


def main():
    for vhost in data['vhosts']:
        vhost_list = get_vhost_list()
        if vhost in vhost_list:
            print('Vhost "%s" already present.' % vhost)
        else:
            check_output(["rabbitmqctl", "add_vhost", vhost]).splitlines()
            print('Vhost "%s" added.' % vhost)


if __name__ == '__main__':
    main()
