from flask_marshmallow.fields import fields

from app import ma


class TokenRequestSchema(ma.Schema):
    access_key = fields.String()
    secret_key = fields.String()
    # class Meta:
    #     # Fields to expose
    #     fields = ("access_key", "secret_key")


token_request_schema = TokenRequestSchema()


class TokenDataTokenSchema(ma.Schema):
    issued_at = fields.String()
    expires_at = fields.String()
    key = fields.String()


class TokenDataSchema(ma.Schema):
    auth_type = fields.String()
    token = fields.Nested(TokenDataTokenSchema())


class TokenResponseSchema(ma.Schema):
    data = fields.Nested(TokenDataSchema())
    # class Meta:
    #     # Fields to expose
    #     fields = ("message", "token", "account_id", "tenant_id", "tenants", "issued_at", "expires_at", "access_token", "refresh_token")


token_response_schema = TokenResponseSchema()


