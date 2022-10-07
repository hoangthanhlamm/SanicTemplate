# http://t.me/check_warning_bot
# https://api.telegram.org/bot2135058445:AAGjZOcK58OAe2nxrb2k8-q0Rk5WpE6NgEo/getUpdates
import time

import telegram

from app.utils.logger_utils import get_logger
from config import TeleBotConfig

logger = get_logger("Telegram Bot")


class TeleBot:
    def __init__(self, bot_token=TeleBotConfig.TOKEN_ID, default_chat_id=TeleBotConfig.BOT_CHAT_IDS, chunk_size=10):
        self._bot_token = bot_token
        chat_ids = [int(str(chat_id).strip()) for chat_id in default_chat_id.split(",")]
        self.chat_ids = chat_ids
        self.telegram_bot = telegram.Bot(bot_token)
        self.messages = []
        self.chunk_size = chunk_size

    def append_message_cache(self, message: str):
        self.messages.append(message)

    def reset_message_cache(self):
        self.messages = []

    def send_message_cache(self):
        chunk_messages = divide_chunks(self.messages, self.chunk_size)
        for chunk_message in chunk_messages:
            merged_message = merge_list_string(chunk_message)
            self.sent_message(merged_message)

    def sent_message(self, message, user_ids=None):
        if not user_ids:
            user_ids = self.get_chat_ids()
        for chat_id in user_ids:
            try:
                retry_fuc(self.telegram_bot.send_message, 3, 40, chat_id, message)
            except Exception as e:
                logger.warning(e)

    def get_chat_ids(self):
        return self.chat_ids


def merge_list_string(list_message):
    _str = ""
    for message in list_message:
        _str += message + "\n"

    return _str


def divide_chunks(l_, n):
    # looping till length l
    for i in range(0, len(l_), n):
        yield l_[i:i + n]


def retry_fuc(fun, max_tries, sleep_time=1, *args):
    for i in range(max_tries):
        try:
            time.sleep(0.3)
            fun(*args)
            break
        except Exception as e:
            logger.warning(e)
            logger.info(f"Sleep {sleep_time}s before retry")
            time.sleep(sleep_time)
            continue
