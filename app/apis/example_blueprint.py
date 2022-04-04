from sanic import Blueprint
from sanic.response import json
from sanic_openapi.openapi2 import doc

from app.decorators.auth import protected
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiUnauthorized
from app.models.name import PostName, name_json_schema
from app.utils.jwt_utils import generate_jwt
from config import Config

example = Blueprint('example_blueprint', url_prefix='/example')


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


@example.route('/set-name', methods={'POST'}, strict_slashes=True)
@doc.tag("Example")
@doc.summary("Set name")
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(PostName, location='body', required=True)
@doc.response(400, {"message": str}, description="Bad Request")
@doc.response(401, {"message": str}, description="Unauthorized")
@validate_with_jsonschema(name_json_schema)
@protected
async def update_bond(request):
    body = request.json
    name = body.get('name')
    return json({
        'message': 'success',
        'detail': f'Hello, {name.title()}'
    })
