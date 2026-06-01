from flask import Blueprint, jsonify, request, g
from DatabaseWrapper import DatabaseWrapper
from auth import require_auth
from utils.decorators import ruolo_richiesto

admin_bp = Blueprint('admin', __name__)
db = DatabaseWrapper()

@admin_bp.route('/utenti', methods=['GET', 'OPTIONS'])
@require_auth
@ruolo_richiesto('admin')
def get_utenti():
    if request.method == "OPTIONS": return jsonify({}), 200
    return jsonify(db.get_utenti_ordinati()), 200

@admin_bp.route('/utenti/<id_utente>/ruolo', methods=['PUT', 'OPTIONS'])
@require_auth
@ruolo_richiesto('admin')
def modifica_ruolo(id_utente):
    if request.method == "OPTIONS": return jsonify({}), 200
    nuovo_ruolo = request.get_json().get('ruolo')
    db.execute_query("UPDATE utente SET ruolo = %s WHERE id_utente = %s", (nuovo_ruolo, id_utente))
    return jsonify({"message": "Ruolo aggiornato"}), 200

@admin_bp.route('/dashboard/stats/<int:id_evento>', methods=['GET', 'OPTIONS'])
@require_auth
@ruolo_richiesto('organizzatore', 'admin')
def get_stats(id_evento):
    if request.method == "OPTIONS": return jsonify({}), 200
    stats = db.get_dashboard_stats(id_evento)
    return jsonify(stats), 200
