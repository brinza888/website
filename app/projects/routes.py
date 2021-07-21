from flask import *

from app.projects import bp


@bp.route('/')
def index():
    return 'Here will be projects view'
