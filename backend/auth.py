from flask import request, jsonify, g
from functools import wraps
import jwt
import requests
import os

# Il link verrà inserito manualmente dopo
KEYCLOAK_URL = "https://potential-xylophone-wr45xgq6gjxcr4-8080.app.github.dev"
REALM = "stafflink-arena"
CLIENT_ID = "stafflink-frontend"

JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

def get_keycloak_public_key(token: str):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    response = requests.get(JWKS_URL)
    jwks = response.json()
    for key_data in jwks["keys"]:
        if key_data["kid"] == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key_data)
    raise Exception("Chiave pubblica non trovata")

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # --- FIX CORS PREFLIGHT ---
        if request.method == "OPTIONS":
            return jsonify({"status": "ok"}), 200
            
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token mancante"}), 401
            
        token = auth_header.split(" ")[1]
        try:
            public_key = get_keycloak_public_key(token)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                #audience=CLIENT_ID, 
                options={"verify_exp": True, "verify_aud": False} 
            )
            g.user = payload
        except Exception as e:
            # Aggiungiamo un print per vedere l'errore esatto nel terminale se fallisce ancora
            print(f"🔴 ERRORE DECODIFICA JWT: {str(e)}") 
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated
