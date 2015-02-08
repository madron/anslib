#!/usr/bin/env python3

from subprocess import check_output
from context import data


def get_user_list():
    user_list = check_output(['rabbitmqctl', 'list_users']).splitlines()
    user_list = [i.decode("utf-8") for i in user_list]
    user_list.remove('Listing users ...')
    user_list = [u.split('\t', 1) for u in user_list]
    user_list = [dict(name=u[0], tags=u[1]) for u in user_list]
    for user in user_list:
        user['tags'] = user['tags'].replace('[', '').replace(']', '').split(', ')
        user['tags'] = [x for x in user['tags'] if x]
        permissions = check_output(["rabbitmqctl", "list_user_permissions", user['name']]).splitlines()
        permissions = [x.decode("utf-8") for x in permissions]
        permissions = [x for x in permissions if not x.startswith('Listing permissions for user')]
        permissions = [x.split('\t') for x in permissions]
        permissions = [(x[0], dict(conf=x[1], write=x[2], read=x[3])) for x in permissions]
        user['permission'] = dict(permissions)
    return user_list


def main():
    for user in data['users']:
        users = get_user_list()
        if user['name'] in [x['name'] for x in users]:
            print('user "%s" already present.' % user['name'])
            check_output(["rabbitmqctl", "change_password", user['name'], user['password']])
        else:
            check_output(["rabbitmqctl", "add_user", user['name'], user['password']])
            print('user "%s" added.' % user['name'])
            users = get_user_list()
        wanted_permission = user.get('permission', dict())
        current_permission = None
        current_tags = None
        for u in users:
            if u['name'] == user['name']:
                current_permission = u['permission']
                current_tags = u['tags']
        # Remove permissions
        for vhost in current_permission.keys():
            if vhost not in wanted_permission.keys():
                check_output(['rabbitmqctl', 'clear_permissions', '-p', vhost, user['name']])
                print('User "%s": removed vhost "%s" permissions' % (user['name'], vhost))
        # Add permissions
        for vhost, permission in wanted_permission.items():
            if vhost in current_permission.keys():
                if not permission == current_permission[vhost]:
                    check_output(['rabbitmqctl', 'set_permissions', '-p', vhost, user['name'],
                        permission['conf'], permission['write'], permission['read']])
                    print('User "%s": updated vhost "%s" permissions' % (user['name'], vhost))
            else:
                check_output(['rabbitmqctl', 'set_permissions', '-p', vhost, user['name'],
                    permission['conf'], permission['write'], permission['read']])
                print('User "%s": added vhost "%s" permissions' % (user['name'], vhost))
        # Tags
        tags = user.get('tags', [])
        if not tags == current_tags:
            command = ['rabbitmqctl', 'set_user_tags', user['name']]
            command = command + tags
            check_output(command)
            print('User "%s": updated tags' % user['name'])


if __name__ == '__main__':
    main()
