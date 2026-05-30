from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt
from DatabaseWrapper import DatabaseWrapper

db = DatabaseWrapper()

def ruolo_richiesto(*ruoli_ammessi):
    """
    Decoratore per limitare l'accesso agli endpoint in base al ruolo.
    Accetta uno o più ruoli (es. 'admin', 'organizzatore').
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token_data = get_jwt()
            id_utente = token_data.get('sub')

            # Recuperiamo il ruolo reale dal nostro database
            utente = db.fetch_one("SELECT ruolo FROM utente WHERE id_utente = %s", (id_utente,))
            
            if not utente or utente['ruolo'] not in ruoli_ammessi:
                return jsonify({"error": f"Accesso negato. Richiesto uno dei seguenti ruoli: {ruoli_ammessi}"}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper