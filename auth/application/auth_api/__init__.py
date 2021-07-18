from flask import Blueprint

bp = Blueprint('auth_api', __name__)

from . import routes