from flask import Blueprint
from pyqiwip2p import QiwiP2P


KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Ijc2O" \
        "GdxNy0wMCIsInVzZXJfaWQiOiI3OTE2OTkyMjIyOCIsInNlY3JldCI6ImU1MWIwNzNhYzNkND" \
        "UyOTFjODkxMWJiMzM2MTNlYTE2MmUxYTY3NjhiMjk2MTFlNzIyMjAzODM1YzA0MTlkY2QifX0="


bp = Blueprint("billing", __name__)
p2p = QiwiP2P(auth_key=KEY)


from app.billing import routes
