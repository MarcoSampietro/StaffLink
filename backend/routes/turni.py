from flask import Blueprint, jsonify, request, g
from DatabaseWrapper import DatabaseWrapper
from auth import require_auth

turni_bp = Blueprint('turni', __name__)
db = DatabaseWrapper()

@turni_bp.route('/disponibili', methods=['GET', 'OPTIONS'])
@require_auth
def disponibili():
    if request.method == "OPTIONS": return jsonify({}), 200
    
    # Recuperiamo l'ID dello steward dal token decodificato
    id_steward = g.user['sub'] 
    
    # Passiamo l'ID alla funzione del database
    turni = db.get_turni_disponibili(id_steward)
    return jsonify(turni), 200

@turni_bp.route('/<int:id_settore>/accetta', methods=['POST', 'OPTIONS'])
@require_auth
def accetta_turno(id_settore):
    if request.method == "OPTIONS": return jsonify({}), 200
    id_steward = g.user['sub']
    try:
        db.execute_query(
            "INSERT INTO turno_assegnato (id_settore, id_steward, stato_candidatura) VALUES (%s, %s, 'in_attesa')",
            (id_settore, id_steward)
        )
        return jsonify({"message": "Turno accettato con successo, in attesa di conferma"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
