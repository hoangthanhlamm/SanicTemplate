import time

import click

from app.constants.cache_constants import CacheConstant
from app.databases.db_cached import DBCached
from app.databases.mongodb import MongoDB
from app.utils.logger_utils import get_logger

logger = get_logger('Refresh Cache')

SLEEP_DURATION = 3  # seconds


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def refresh_cache():
    """Refresh api for optimize api."""
    _db = MongoDB()
    logger.info(f'Connected to graph {_db.connection_url}')

    cached = DBCached()

    while True:
        try:
            config = _db.get_config()
            next_synced_timestamp = config.next_synced_timestamp
            current_time = int(time.time())
            if current_time < next_synced_timestamp:
                sleep_time = next_synced_timestamp - current_time
                logger.info(f'Sleep {sleep_time} seconds ...')
                time.sleep(sleep_time)

                current_time = int(time.time())

            config.next_synced_timestamp = current_time + 900
            cached.save_cached({CacheConstant.configs: config.to_dict()})
            logger.info(f'Saved api, took {round(time.time() - current_time, 3)}s')
        except Exception as ex:
            logger.exception(ex)
            logger.warning(f'Something went wrong!!! Try again after {SLEEP_DURATION} seconds ...')
