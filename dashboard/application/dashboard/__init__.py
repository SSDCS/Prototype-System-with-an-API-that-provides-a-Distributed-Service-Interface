from flask import Blueprint

bp = Blueprint('dashboard', __name__, static_folder="./static", template_folder="./templates")

from . import routes