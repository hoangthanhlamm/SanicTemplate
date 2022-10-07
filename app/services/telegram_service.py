from telegram import Bot

from app.utils.logger_utils import get_logger
from config import NotifierConfig

logger = get_logger('Telegram Service')


class TelegramService:
    __instance = None

    @staticmethod
    def get_instance():
        if TelegramService.__instance is None:
            TelegramService()
        return TelegramService.__instance

    def __init__(self, notifier_token=None):
        if TelegramService.__instance is not None:
            raise Exception('This class is a singleton!')

        TelegramService.__instance = self

        token = notifier_token if notifier_token else NotifierConfig.TELEGRAM_BOT_TOKEN
        self.bot = Bot(token)

    def send(self, chat_id, text):
        return self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='MarkdownV2',
            disable_web_page_preview=True
        )


def reformat_message_telegram(msg: str):
    msg = msg.replace('.', '\.').replace('-', '\-').replace('+', '\+').replace('_', '\_')
    msg = msg.replace('|', '\|')
    # msg = msg.replace('(', '\(').replace(')', '\)')
    return msg
