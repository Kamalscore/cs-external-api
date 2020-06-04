# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from flask import jsonify

from app import app


def to_error(msg):
    return {"message": msg}


@app.errorhandler(405)
def resource_not_found(e):
    print(e)
    return jsonify(error=to_error(e)), 405
