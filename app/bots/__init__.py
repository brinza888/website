from flask import Blueprint


bp = Blueprint("bots", __name__)


from app.bots import routes
