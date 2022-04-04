import time

from app.constants.mongodb_constants import MongoKeys


class Config:
    def __init__(self):
        self.key = MongoKeys.config
        self.next_synced_timestamp = 0

    def to_dict(self):
        return {
            '_id': self.key,
            'next_synced_timestamp': self.next_synced_timestamp
        }


def json_dict_to_config(json_dict):
    config = Config()
    if not json_dict:
        return config

    config.next_synced_timestamp = json_dict.get('next_synced_timestamp', int(time.time()))
    return config
