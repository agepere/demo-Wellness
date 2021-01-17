from flask import Blueprint, make_response, request, jsonify
from models import User
from sqlalchemy import exc
from database import setup_mysql_engine_default
from sqlalchemy.orm import sessionmaker
from functools import wraps
import hashlib
import jwt
import yaml

with open('config.yml', 'r') as ymlConf:
    configuration = yaml.safe_load(ymlConf)

auth_api = Blueprint('auth', __name__)

ERROR_MESSAGE = 'There was an unexpected error, please try again later'


@auth_api.route('/signup', methods=['POST'])
def auth():
    engine_db = None
    s = None
    response = None

    try:
        engine_db = setup_mysql_engine_default()
        session = sessionmaker(bind=engine_db)
        s = session()

        user = User(username=request.json['username'], password=hash_pass(request.json['password']))

        s.add(user)
        s.commit()

        response = make_response(jsonify(user), 200)
    except exc.IntegrityError:
        response = make_response({'message': 'That username already exists'}, 400)
    except:
        response = make_response({'message': ERROR_MESSAGE}, 500)
    finally:
        # Clean resources and return the response
        if s is not None:
            s.close()
        if engine_db is not None:
            engine_db.dispose()

        if response is not None:
            return response
        else:
            return make_response({'message': ERROR_MESSAGE}, 500)


@auth_api.route('/login', methods=['POST'])
def login():
    engine_db = None
    s = None
    response = None

    try:
        engine_db = setup_mysql_engine_default()
        session = sessionmaker(bind=engine_db)
        s = session()
        user = s.query(User).filter(User.username == request.json['username']).filter(
            User.password == hash_pass(request.json['password'])).first()

        if user is None:
            response = make_response({'message': 'Invalid username or password'}, 400)
        else:
            token = jwt.encode({'id': user.id}, configuration['api']['jwtSecret'])
            response = make_response({'token': token}, 200)

    except:
        response = make_response({'message': ERROR_MESSAGE}, 500)
    finally:
        # Clean resources and return the response
        if s is not None:
            s.close()
        if engine_db is not None:
            engine_db.dispose()

        if response is not None:
            return response
        else:
            return make_response({'message': ERROR_MESSAGE}, 500)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        engine_db = None
        s = None
        response = None
        user = None

        try:
            # Get the bearer token
            token = request.headers['authorization'][6:].strip()

            data = jwt.decode(token, configuration['api']['jwtSecret'], algorithms=["HS256"])

            engine_db = setup_mysql_engine_default()
            session = sessionmaker(bind=engine_db)
            s = session()

            user = s.query(User).filter(User.id == data['id']).first()

            if not user:
                response = make_response({'message': 'You must log in'}, 401)
        except:
            response = make_response({'message': 'You must log in'}, 401)
        finally:
            if s is not None:
                s.close()
            if engine_db is not None:
                engine_db.dispose()

            if response is not None:
                return response
            else:
                return f(user, *args, **kwargs)

    return decorated


@auth_api.route('/', methods=['GET'])
@token_required
def principal(user):
    return make_response(jsonify(user), 200)


def hash_pass(password):
    return str(hashlib.sha256(password.encode()).hexdigest())
