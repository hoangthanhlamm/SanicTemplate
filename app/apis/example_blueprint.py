import time

from sanic import Blueprint
from sanic.response import json
from sanic_openapi.openapi2 import doc

from app.databases.db_cached import DBCached
from app.databases.mongodb import MongoDB
from app.decorators.auth import protected
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiUnauthorized
from app.models.config import PostConfig, config_json_schema, json_dict_to_config
from app.services.queue.tasks import task_send_mail
from app.utils.jwt_utils import generate_jwt
from app.utils.logger_utils import get_logger
from config import Config

logger = get_logger('Example API')

example = Blueprint('example_blueprint', url_prefix='/example')

_db = MongoDB()


@example.route('/get-jwt', methods={'GET'})
@doc.tag("Example")
@doc.summary("Get JWT")
@doc.consumes(doc.String(name="password", description="Password for generate jwt"), location="query", required=True)
@doc.response(401, {"message": str}, description="Unauthorized")
async def get_jwt(request):
    password = request.args.get("password")
    if password != Config.JWT_PASSWORD:
        raise ApiUnauthorized("Wrong password")
    token = generate_jwt()
    return json({'token': str(token)})


@example.route('/get-config', methods={'GET'})
@doc.tag("Example")
@doc.summary("Get config")
async def get_config(request):
    _cached = DBCached(read_only=True)
    config = _cached.get_config()
    if not config:
        config = _db.get_config()
        config = config.to_dict()

    if '_id' in config:
        config.pop('_id')
    return json({'config': config})


@example.route('/update-config', methods={'POST'}, strict_slashes=True)
@doc.tag("Example")
@doc.summary("Update config")
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(PostConfig, location='body', required=True)
@doc.response(400, {"message": str}, description="Bad Request")
@doc.response(401, {"message": str}, description="Unauthorized")
@validate_with_jsonschema(config_json_schema)
@protected
async def update_config(request):
    body = request.json
    config = json_dict_to_config(body)
    _db.set_config(config)
    return json({
        'message': 'success',
    })


@example.route('/email/register', methods={'POST'})
@doc.tag("Example")
@doc.summary("Send mail with queue")
@doc.consumes(doc.String(name="email", description="Email"), location="query", required=True)
async def register_email(request):
    email_address = request.args.get('email')
    mail = {
        'recipients': [email_address],
        'subject': f'Register {str(int(time.time()))[-3:]}',
        'html': """
            <p>Thank you for your subscribe!</>
        """
    }

    # Use RabbitMQ to send mail background
    task_send_mail.delay(mail)

    return json({'status': 'success'})
