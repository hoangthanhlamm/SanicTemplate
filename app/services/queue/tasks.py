from app.databases.mongodb import MongoDB
from app.services.email_service import EmailService
from app.services.queue.worker import app
from app.services.telegram_service import TelegramService
from app.utils.logger_utils import get_logger

logger = get_logger('Queue Tasks')

_db = MongoDB()


@app.task(name='send_mail')
def task_send_mail(mail):
    email_service = EmailService()
    email_service.send(
        recipients=mail['recipients'],
        subject=mail['subject'],
        html=mail['html']
    )


@app.task(name='send_tele')
def task_send_tele(message):
    telegram_service = TelegramService.get_instance()
    telegram_service.send(
        chat_id=message['chat_id'],
        text=message['text']
    )
