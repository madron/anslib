import json
import os


data = dict(
    servers=json.loads(os.getenv('servers', '[]')),
    username=os.getenv('username', ''),
    password=os.getenv('password', ''),
)
