import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from routes import auth_bp, turni_bp, admin_bp
load_dotenv()

app = Flask(__name__)

# Configurazione JWT (La chiave segreta deve essere complessa in produzione)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'chiave-super-segreta-stafflink')
# Diciamo a Flask dove cercare il token (negli header HTTP come "Bearer <token>")
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

# Gestione globale degli errori JWT
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Autenticazione richiesta. Token mancante."}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Token non valido."}), 401

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(turni_bp, url_prefix='/api/turni')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Backend StaffLink Arena operativo!"}), 200

if __name__ == '__main__':
    # In esecuzione su porta 5000 (standard per Flask)
    app.run(host='0.0.0.0', port=5000, debug=True)