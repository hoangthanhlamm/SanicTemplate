from celery import Celery

from config import RabbitMQConfig

app = Celery(
    "example-worker",
    broker=f'amqp://{RabbitMQConfig.USERNAME}:{RabbitMQConfig.PASSWORD}@{RabbitMQConfig.HOST}:{RabbitMQConfig.PORT}//',
    imports=["app.services.queue.tasks"]
)

app.conf.task_default_queue = 'example'
app.conf.broker_transport_options = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.2,
}
app.conf.update(
    task_annotations={
        'send_mail': {
            'rate_limit': '6/m'
        },
        'send_tele': {
            'rate_limit': '30/m'
        }
    }
)
