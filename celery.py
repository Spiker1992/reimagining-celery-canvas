from celery import Celery

# RabbitMQ broker URL
broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'

# Create Celery app with RabbitMQ broker
app = Celery('my_app', broker=broker_url)