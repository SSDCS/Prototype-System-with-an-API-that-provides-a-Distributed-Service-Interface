from flask import Blueprint

bp = Blueprint('dashboard', __name__)

from dashboard.application.dashboard import routes