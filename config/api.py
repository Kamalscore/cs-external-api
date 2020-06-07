from flask_restplus import Api, OrderedModel, Model
from flask_restplus.utils import default_id
from werkzeug.utils import cached_property

from config.swagger import CustomSwagger


class CustomizedApi(Api):
    """
        The main entry point for the application.
        You need to initialize it with a Flask Application: ::

        >>> app = Flask(__name__)
        >>> api = Api(app)

        Alternatively, you can use :meth:`init_app` to set the Flask application
        after it has been constructed.

        The endpoint parameter prefix all views and resources:

            - The API root/documentation will be ``{endpoint}.root``
            - A resource registered as 'resource' will be available as ``{endpoint}.resource``

        :param flask.Flask|flask.Blueprint app: the Flask application object or a Blueprint
        :param str version: The API version (used in Swagger documentation)
        :param str title: The API title (used in Swagger documentation)
        :param str description: The API description (used in Swagger documentation)
        :param str terms_url: The API terms page URL (used in Swagger documentation)
        :param str contact: A contact email for the API (used in Swagger documentation)
        :param str license: The license associated to the API (used in Swagger documentation)
        :param str license_url: The license page URL (used in Swagger documentation)
        :param str endpoint: The API base endpoint (default to 'api).
        :param str default: The default namespace base name (default to 'default')
        :param str default_label: The default namespace label (used in Swagger documentation)
        :param str default_mediatype: The default media type to return
        :param bool validate: Whether or not the API should perform input payload validation.
        :param bool ordered: Whether or not preserve order models and marshalling.
        :param str doc: The documentation path. If set to a false value, documentation is disabled.
                    (Default to '/')
        :param list decorators: Decorators to attach to every resource
        :param bool catch_all_404s: Use :meth:`handle_error`
            to handle 404 errors throughout your app
        :param dict authorizations: A Swagger Authorizations declaration as dictionary
        :param bool serve_challenge_on_401: Serve basic authentication challenge with 401
            responses (default 'False')
        :param FormatChecker format_checker: A jsonschema.FormatChecker object that is hooked into
            the Model validator. A default or a custom FormatChecker can be provided (e.g., with custom
            checkers), otherwise the default action is to not enforce any format validation.
        """

    def __init__(self, app=None, version='1.0', title=None, description=None, terms_url=None, license=None,
                 license_url=None, contact=None, contact_url=None, contact_email=None, authorizations=None,
                 security=None, doc='/', default_id=default_id, default='default', default_label='Default namespace',
                 validate=None, tags=None, prefix='', ordered=False, default_mediatype='application/json',
                 decorators=None, catch_all_404s=False, serve_challenge_on_401=False, format_checker=None, **kwargs):
        super(CustomizedApi, self).__init__(app, version, title, description, terms_url, license, license_url, contact, contact_url,
                         contact_email, authorizations, security, doc, default_id, default, default_label, validate,
                         tags, prefix, ordered, default_mediatype, decorators, catch_all_404s, serve_challenge_on_401,
                         format_checker, **kwargs)
        self.for_doc_alone_model_names = []

    @cached_property
    def __schema__(self):
        """
        The Swagger specifications/schema for this API

        :returns dict: the schema as a serializable dict
        """
        if not self._schema:
            try:
                self._schema = CustomSwagger(self).as_dict()
            except Exception:
                # Log the source exception for debugging purpose
                # and return an error message
                msg = 'Unable to render schema'
                super(CustomizedApi, self).log.exception(msg)  # This will provide a full traceback
                return {'error': msg}
        return self._schema

    def model(self, name=None, model=None, mask=None, for_doc_alone=False, **kwargs):
        """
        Register a model

        .. seealso:: :class:`Model`
        """
        cls = OrderedModel if self.ordered else Model
        model = cls(name, model, mask=mask)
        model.__apidoc__.update(kwargs)
        if for_doc_alone:
            self.for_doc_alone_model_names.append(name)
        return self.add_model(name, model)

