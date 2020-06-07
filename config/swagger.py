from collections import OrderedDict

from flask_restplus import Swagger
from flask_restplus.model import ModelBase
from flask_restplus.reqparse import RequestParser
from flask_restplus.utils import not_none


class CustomSwagger(Swagger):

    """
    A Swagger documentation wrapper for an API instance.
    """
    def __init__(self, api):
        super(CustomSwagger, self).__init__(api)
        for name in self.api.for_doc_alone_model_names:
            super(CustomSwagger, self).register_model(self.api.models[name])
        self.api = api

    def expected_params(self, doc):
        params = OrderedDict()
        if 'expect' not in doc:
            return params

        for expect in doc.get('expect', []):
            if isinstance(expect, RequestParser):
                parser_params = OrderedDict((p['name'], p) for p in expect.__schema__)
                params.update(parser_params)
            elif isinstance(expect, ModelBase):
                name = expect.name if hasattr(expect, 'name') else 'payload'
                params[name] = not_none({
                    'name': expect.name if hasattr(expect, 'name') else 'payload',
                    'required': True,
                    'in': 'body',
                    'schema': self.serialize_schema(expect),
                })
            elif isinstance(expect, (list, tuple)):
                if len(expect) == 2:
                    # this is (payload, description) shortcut
                    model, description = expect
                    params['payload'] = not_none({
                        'name': 'payload',
                        'required': True,
                        'in': 'body',
                        'schema': self.serialize_schema(model),
                        'description': description
                    })
                else:
                    params['payload'] = not_none({
                        'name': 'payload',
                        'required': True,
                        'in': 'body',
                        'schema': self.serialize_schema(expect),
                    })
        return params
