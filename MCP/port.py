from flask import Flask, jsonify
import os
from pyngrok import ngrok
from flask_cors import CORS

NGROK_AUTH_TOKEN="32IoJ7JXDYi11egrghJ4nRTSVXO_5xbQPaMwQqyG596jeCx5V"


app = Flask(__name__)
CORS(app)



@app.route('/api/hello', methods=["GET"])
def hello():
    return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 7001))
    os.environ['FLASK_ENV'] = 'development'
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(port)
    print("Starting ngrok...",public_url)
    app.run(port=port)
    