from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections, MongoIndex, MongoKeys
from app.models.config import json_dict_to_config, Config
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'

        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]

        self._configs_col = self.db[MongoCollections.configs]

        self._create_index()

    def _create_index(self):
        if MongoIndex.address_configs not in self._configs_col.index_information():
            self._configs_col.create_index([('address', 'hashed')], name=MongoIndex.address_configs)
        logger.info('Indexed !!!')

    def get_config(self):
        try:
            filter_ = {'_id': MongoKeys.config}
            info = self._configs_col.find_one(filter_)
            config = json_dict_to_config(info)
            return config
        except Exception as ex:
            logger.exception(ex)
        return None

    def set_config_with_dict(self, config_dict):
        try:
            filter_ = {'_id': MongoKeys.config}
            config_dict.update(filter_)
            data = {'$set': config_dict}
            self._configs_col.update_one(filter_, data, upsert=True)
        except Exception as ex:
            logger.exception(ex)

    def set_config(self, config: Config):
        try:
            filter_ = {'_id': MongoKeys.config}
            data = {'$set': config.to_dict()}
            self._configs_col.update_one(filter_, data, upsert=True)
        except Exception as ex:
            logger.exception(ex)
