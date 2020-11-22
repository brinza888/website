from app import create_app
from app.tools import *


app = create_app()


if __name__ == '__main__':
    app.run(host="192.168.2.43", port=5000, debug=True)
