from flask import Blueprint

iris = Blueprint('iris', __name__)

from . import views