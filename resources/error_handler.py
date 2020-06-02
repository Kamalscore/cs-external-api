from flask import jsonify

from app import app


def to_error(msg):
    return {"message": msg}


@app.errorhandler(405)
def resource_not_found(e):
    print(e)
    return jsonify(error=to_error(e)), 405
