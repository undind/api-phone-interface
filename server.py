import config
from flask_cors import CORS

connex_app = config.connex_app

connex_app.add_api("api.yml")

CORS(connex_app.app)

# Run Server
if __name__ == '__main__':
  connex_app.run(host='localhost', debug=True)
