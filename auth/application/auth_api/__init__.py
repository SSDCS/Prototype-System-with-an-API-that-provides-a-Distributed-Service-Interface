from flask import Blueprint

bp = Blueprint('auth_api', __name__)

from auth.application.auth_api import routes