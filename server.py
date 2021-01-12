from flask import Flask, request, make_response
from flask_restful import Api
from flask_jsonpify import jsonify
import yaml
from auth import auth_api

with open('config.yml', 'r') as ymlConf:
    configuration = yaml.load(ymlConf)

app = Flask(__name__)
api = Api(app)


if __name__ == '__main__':
    app.register_blueprint(auth_api, url_prefix='/login')

    app.run(host=configuration['api']['host'], port=configuration['api']['port'])
