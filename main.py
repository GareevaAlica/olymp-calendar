from app import app, db
from config import host, port, debug
import os

if __name__ == '__main__':
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host=host, port=port, debug=debug)
