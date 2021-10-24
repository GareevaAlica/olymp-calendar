from app import app
from config import host, port, debug
import os

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host=host, port=port, debug=debug)
