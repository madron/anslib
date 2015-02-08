import json
import os


data = dict(
    default_vhost=os.getenv('default_vhost', '/'),
    default_user=os.getenv('default_user', 'admin'),
    default_pass=os.getenv('default_pass', 'admin'),
    vhosts=json.loads(os.getenv('vhosts', '[]')),
    users=json.loads(os.getenv('users', '[]')),
)
