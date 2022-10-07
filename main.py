import os
import time

from sanic.response import text
from sanic_openapi import doc, openapi2_blueprint

from app import create_app
from app.apis import api
from app.misc.log import log
from config import Config, LocalDBConfig

app = create_app(Config, LocalDBConfig)
app.blueprint(openapi2_blueprint)
app.config["API_HOST"] = Config.API_HOST
app.config["API_SCHEMES"] = Config.API_SCHEMES
app.config["API_TITLE"] = Config.API_TITLE
app.config["API_VERSION"] = Config.API_VERSION
app.config["API_DESCRIPTION"] = Config.API_DESCRIPTION
app.config["API_CONTACT_EMAIL"] = Config.API_CONTACT_EMAIL

app.config["RESPONSE_TIMEOUT"] = Config.RESPONSE_TIMEOUT

app.blueprint(api)


@app.route("/ping", methods={'GET'})
@doc.tag("Ping")
@doc.summary("Ping server !")
async def hello_world(request):
    return text("Hello World")


@app.middleware('request')
async def add_start_time(request):
    request.headers['start_time'] = time.time()


@app.middleware('response')
async def add_spent_time(request, response):
    try:
        if 'start_time' in request.headers:
            timestamp = request.headers['start_time']
            spend_time = round((time.time() - timestamp), 3)
            log("{} {} {} {} {}s".format(response.status, request.method, request.path, request.query_string, spend_time))
    except Exception as ex:
        log(ex.__str__(), 'ERROR')


if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        log(
            message='SECRET KEY is not set in the environment variable.',
            keyword='WARN'
        )

    app.run(**app.config['RUN_SETTING'])
