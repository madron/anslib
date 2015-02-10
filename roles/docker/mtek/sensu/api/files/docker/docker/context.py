import os


ssl = os.getenv('rabbitmq_ssl', 'false').lower()
if ssl in ('yes', 'true'):
    rabbitmq_ssl = True
    rabbitmq_port = 5671
else:
    rabbitmq_ssl = False
    rabbitmq_port = 5672


data = dict(
    rabbitmq_host=os.getenv('rabbitmq_host', 'rabbitmq'),
    rabbitmq_port=os.getenv('rabbitmq_port', rabbitmq_port),
    rabbitmq_ssl=rabbitmq_ssl,
    rabbitmq_sensu_server_password=os.getenv('rabbitmq_sensu_server_password', 'sensu'),
    api_password=os.getenv('api_password', 'admin'),
)
