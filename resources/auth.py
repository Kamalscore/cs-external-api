import logging

from flask import request, abort
from flask_restplus import Resource, marshal, fields

from client import get_token
from models.swagger_models import auth_request, auth_response, token, error, auth_tenant_model, auth_detailed_response, wild_card_model

from app import api
from utils.HelperUtils import getClassName

auth_name_space = api.namespace(name='Tokens', path="/", description='Manage Tokens')
tokenModel = api.model('Token', token())
authTenantModel = api.model('TokenTenantModel', auth_tenant_model())
requestModel = api.model('AuthRequest', auth_request())
wildcardModel = api.model('Dict', wild_card_model())
responseModel = api.model('AuthResponse', auth_response(tokenModel, authTenantModel, wildcardModel))
# responseDetailedModel = api.model('AuthDetailedResponse', auth_detailed_response(tokenModel, wildcardModel))
responseDetailedModel = api.inherit('AuthDetailedResponse', responseModel, {'data': fields.Nested(wildcardModel, required=True, description="Complete Data.")})
errorModel = api.model('Error', error())


@auth_name_space.route("/v1/auth/tokens")
class AuthResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(AuthResource))

    @api.doc(name="Auth Request", description="<u><b>Authentication Request</b></u>: Fetches the token. Below "
                                              "mentioned model is the detailed one, that's obtained when the flag "
                                              "<i><b>is_detail_required</b></i> "
                                              "is <i>true</i>. Please find the model: <b>AuthResponse</b>, when the "
                                              "flag is <i>false</i>.",
             params={'is_detail_required': {'description': 'Whether detailed response required or not.',
                                            'in': 'query', 'type': 'bool', 'default':False}})
    @api.expect(requestModel, validate=True)
    @auth_name_space.response(model=responseDetailedModel, code=201, description='Created')
    @auth_name_space.response(model=responseModel, code=201, description='Created')
    @auth_name_space.response(model=errorModel, code=400, description='Bad Request')
    @auth_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @auth_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            is_detail_required = bool(request.args.get('is_detail_required'))
            print(request.json)
            response = get_token(request.json["access_key"], request.json["secret_key"])
            if response.status_code == 200:
                return marshal(response.json(), responseDetailedModel if is_detail_required else responseModel), 201
            else:
                # TODO Need to raise the proper errors by checking the status like 400, 401, 403 etc...
                raise abort(response.text.encode('utf8'))
        except KeyError as e:
            auth_name_space.abort(500, e.__doc__, status=e, statusCode="500")
