from flask import Blueprint

# Definiamo i blueprint
auth_bp = Blueprint('auth', __name__)
turni_bp = Blueprint('turni', __name__)
admin_bp = Blueprint('admin', __name__)

# Importiamo le viste (routes) in modo che vengano registrate sui blueprint
# Nota: L'import viene fatto *dopo* la definizione del Blueprint per evitare dipendenze circolari
from . import auth, turni, admin