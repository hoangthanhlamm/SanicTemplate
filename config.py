import os


class Config:
    RUN_SETTING = {
        'host': os.environ.get('SERVER_HOST', 'localhost'),
        'port': int(os.environ.get('SERVER_PORT', 8080)),
        'debug': False,
        "access_log": True,
        "auto_reload": True,
        'workers': 4
    }
    # uWSGI를 통해 배포되어야 하므로, production level에선 run setting을 건드리지 않음

    SECRET_KEY = os.environ.get('SECRET_KEY', 'example project')
    JWT_PASSWORD = os.getenv('JWT_PASSWORD', 'dev123')
    EXPIRATION_JWT = 3600  # seconds
    RESPONSE_TIMEOUT = 900  # seconds

    API_HOST = os.getenv('API_HOST', '0.0.0.0:8096')
    API_SCHEMES = os.getenv('API_SCHEMES', 'http')
    API_VERSION = os.getenv('API_VERSION', '0.1.0')
    API_TITLE = os.getenv('API_TITLE', 'Example API')
    API_DESCRIPTION = os.getenv('API_DESCRIPTION', 'Swagger for Example API')
    API_CONTACT_EMAIL = os.getenv('API_CONTACT_EMAIL', 'example@gmail.com')


class LocalDBConfig:
    pass


class RemoteDBConfig:
    pass


class MongoDBConfig:
    USERNAME = os.environ.get("MONGO_USERNAME") or "just_for_dev"
    PASSWORD = os.environ.get("MONGO_PASSWORD") or "password_for_dev"
    HOST = os.environ.get("MONGO_HOST") or "localhost"
    PORT = os.environ.get("MONGO_PORT") or "27017"
    DATABASE = "example_db"


class TeleBotConfig:
    TOKEN_ID = os.getenv("TELE_BOT_TOKEN_ID") or "123456789:AAGjZOcK58OAe2nxrb2k8-q0Rk5WpE6NgEo"
    BOT_CHAT_IDS = os.getenv("TELE_BOT_CHAT_IDS") or "12345,123456"
