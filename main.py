from flask import Blueprint
from flask import *

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.route('/')
def main():
    return 'This is main page'