from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from DatabaseWrapper import DatabaseWrapper
from . import auth_bp

# Istanziamo il DatabaseWrapper
db = DatabaseWrapper()

@auth_bp.route('/sync', methods=['POST'])
@jwt_required()
def sync_utente():
    """
    Sincronizza i dati dell'utente dal token JWT al database MySQL.
    Se l'utente non esiste, lo crea.
    """
    token_data = get_jwt()
    
    # Estraiamo i dati forniti da Keycloak
    id_utente = token_data.get('sub')
    
    # Gestione del cognome/nome: Keycloak usa spesso "family_name" e "given_name"
    # oppure il nome completo in "name" se non sono valorizzati
    cognome = token_data.get('family_name')
    nome = token_data.get('given_name')
    email = token_data.get('email')

    # Se cognome o nome mancano nel token, proviamo a estrarli dal campo 'name'
    if not cognome or not nome:
        nome_completo = token_data.get('name', '').split(' ')
        if len(nome_completo) > 1:
            nome = nome_completo[0]
            cognome = ' '.join(nome_completo[1:])
        else:
            nome = token_data.get('name', 'Sconosciuto')
            cognome = 'Sconosciuto'

    # Verifichiamo se l'utente esiste già nel DB
    query_check = "SELECT id_utente FROM utente WHERE id_utente = %s"
    utente_esistente = db.fetch_one(query_check, (id_utente,))
    
    if not utente_esistente:
        try:
            # Creiamo l'utente assegnandogli di default il ruolo 'steward'
            query_insert = """
                INSERT INTO utente (id_utente, cognome, nome, email, ruolo) 
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_query(query_insert, (id_utente, cognome, nome, email, 'steward'))
            return jsonify({"message": "Utente sincronizzato nel DB con successo!", "status": "created"}), 201
        except Exception as e:
            current_app.logger.error(f"Errore durante la sincronizzazione utente: {e}")
            return jsonify({"error": "Errore durante il salvataggio dell'utente."}), 500
            
    return jsonify({"message": "Utente già allineato.", "status": "synced"}), 200