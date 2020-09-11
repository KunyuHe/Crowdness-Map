import logging

from flask import Blueprint

bp = Blueprint("api_userlog", __name__, url_prefix='/userlog')
logger = logging.getLogger(__name__)
