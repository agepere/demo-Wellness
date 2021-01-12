from flask import Blueprint, make_response

auth_api = Blueprint('auth', __name__)


@auth_api.route('/')
def auth():
    return make_response({'ok': 'ok'}, 200)
