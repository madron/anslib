import os


ssl = os.getenv('ssl', 'false').lower()
if ssl in ('yes', 'true'):
    ssl = True
    rabbitmq_port = 5671
else:
    ssl = False
    rabbitmq_port = 5672


data = dict(
    rabbitmq_ssl=ssl,
    rabbitmq_port=rabbitmq_port,
    rabbitmq_password=os.getenv('rabbitmq_password', 'sensu'),
    api_password=os.getenv('api_password', 'admin'),
)
