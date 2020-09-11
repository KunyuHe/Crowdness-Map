import logging
import logging.config
import os

import yaml
from app.api.router import router
from app.utils.core import JSONEncoder
from app.utils.util import create_dir, read_yaml
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)


def create_app(config_name, config_path=None):
    app = Flask(__name__)

    # Cross-domain
    CORS(app, resources=r"/*")

    # Read APP config
    if not config_path:
        pwd = os.getcwd()
        config_path = os.path.join(pwd, 'config/config.yaml')
    if not config_name:
        config_name = 'PRODUCTION'
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    # Register API
    register_api(app=app, routers=router)

    app.json_encoder = JSONEncoder

    # Logging directory and configuration
    create_dir(app.config['LOGGING_PATH'])
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)

    # Message
    with open(app.config['RESPONSE_MESSAGE'], 'r', encoding='utf-8') as f:
        msg = yaml.safe_load(f.read())
        app.config.update(msg)

    return app


def create_socketio(app):
    app.config['SECRET_KEY'] = 'secret!'

    socketio = SocketIO(app, cors_allowed_origins="*")

    return socketio


def register_form(app, router_api, url, method, view_func):
    if method in router_api.__methods__:
        app.add_url_rule('{}<string:key>'.format(url), view_func=view_func,
                         methods=[method, ])


def register_api(app, routers):
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            try:
                endpoint = router_api.__name__
                view_func = router_api.as_view(endpoint)
                # url默认为类名小写
                url = '/{}/'.format(router_api.__name__.lower())
                if 'GET' in router_api.__methods__:
                    app.add_url_rule(url, defaults={'key': None},
                                     view_func=view_func, methods=['GET', ])
                    register_form(app, router_api, url, "GET", view_func)
                if 'POST' in router_api.__methods__:
                    app.add_url_rule(url, view_func=view_func,
                                     methods=['POST', ])
                register_form(app, router_api, url, "PUT", view_func)
                register_form(app, router_api, url, "DELETE", view_func)
            except Exception as e:
                raise ValueError(e)
