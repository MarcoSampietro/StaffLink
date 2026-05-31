from flask import Blueprint, jsonify, request, g
from DatabaseWrapper import DatabaseWrapper
from auth import require_auth

auth_bp = Blueprint('auth', __name__)
db = DatabaseWrapper()

@auth_bp.route('/sync', methods=['POST', 'OPTIONS'])
@require_auth
def sync_utente():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    token_data = g.user
    id_utente = token_data.get('sub')
    
    cognome = token_data.get('family_name', 'Utente')
    nome = token_data.get('given_name', token_data.get('preferred_username', 'Sconosciuto'))
    email = token_data.get('email', f"{nome.lower()}@stafflink.com")

    ruoli_keycloak = token_data.get('realm_access', {}).get('roles', [])
    ruolo_db = 'steward'
    if 'admin' in ruoli_keycloak:
        ruolo_db = 'admin'
    elif 'organizzatore' in ruoli_keycloak:
        ruolo_db = 'organizzatore'

    if not db.fetch_one("SELECT id_utente FROM utente WHERE id_utente = %s", (id_utente,)):
        db.execute_query("INSERT INTO utente (id_utente, cognome, nome, email, ruolo) VALUES (%s, %s, %s, %s, %s)", 
                         (id_utente, cognome, nome, email, ruolo_db))
        return jsonify({"message": "Utente inserito!"}), 201
    else:
        db.execute_query("UPDATE utente SET ruolo = %s, nome = %s, cognome = %s WHERE id_utente = %s", 
                         (ruolo_db, nome, cognome, id_utente))
        return jsonify({"message": "Utente allineato."}), 200
