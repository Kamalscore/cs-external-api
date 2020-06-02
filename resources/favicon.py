import logging
import os

from flask import send_from_directory
from flask_restplus import Resource

from app import app
from resources.auth import auth_name_space as fav_name_space
from utils.HelperUtils import getClassName


@fav_name_space.route('/swaggerui/favicon-16x16.png', doc=False)
class Fav16(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(Fav16))

    def get(self):
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon-16x16.png', mimetype='image/vnd.microsoft.icon')


@fav_name_space.route('/swaggerui/favicon-32x32.png', doc=False)
class Fav32(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(Fav32))

    def get(self):
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon-16x16.png', mimetype='image/vnd.microsoft.icon')
