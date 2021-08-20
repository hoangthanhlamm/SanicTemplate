import os

from sanic.response import text

from app import create_app
from app.apis import api
from app.misc.log import log
from config import Config, LocalDBConfig

app = create_app(Config, LocalDBConfig)


@app.route("/hello-world", methods={'GET', 'POST'})
async def hello_world(request):
    return text("Hello World")


if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        log(message='SECRET KEY is not set in the environment variable.',
            keyword='WARN')
    app.blueprint(api)
    app.run(**app.config['RUN_SETTING'])
