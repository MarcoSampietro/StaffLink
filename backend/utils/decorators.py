from functools import wraps
from flask import jsonify, g
from DatabaseWrapper import DatabaseWrapper

db = DatabaseWrapper()

def ruolo_richiesto(*ruoli_ammessi):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            id_utente = g.user.get('sub')
            utente = db.fetch_one("SELECT ruolo FROM utente WHERE id_utente = %s", (id_utente,))
            if not utente or utente['ruolo'] not in ruoli_ammessi:
                return jsonify({"error": f"Accesso negato. Richiesto: {ruoli_ammessi}"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
