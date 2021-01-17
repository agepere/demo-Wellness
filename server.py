from flask import Flask
from flask_restful import Api
import yaml
from auth import auth_api
from energy import energy_api

with open('config.yml', 'r') as ymlConf:
    configuration = yaml.safe_load(ymlConf)

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.register_blueprint(auth_api, url_prefix='/user')
    app.register_blueprint(energy_api, url_prefix='/energy')

    app.run(host=configuration['api']['host'], port=configuration['api']['port'])
