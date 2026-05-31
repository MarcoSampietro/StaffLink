import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.turni import turni_bp

load_dotenv()

app = Flask(__name__)
# Configurazione CORS globale corazzata
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(turni_bp, url_prefix='/api/turni')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
