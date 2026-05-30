from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from DatabaseWrapper import DatabaseWrapper
from utils.decorators import ruolo_richiesto
from . import admin_bp

db = DatabaseWrapper()

# --- 1. CREAZIONE EVENTI ---

@admin_bp.route('/eventi', methods=['POST'])
@jwt_required()
@ruolo_richiesto('organizzatore', 'admin') 
def crea_evento():
    """Crea un nuovo evento."""
    dati = request.get_json()
    titolo = dati.get('titolo')
    data_inizio = dati.get('data_inizio')
    data_fine = dati.get('data_fine')
    path_planimetria = dati.get('path_planimetria', '')

    if not all([titolo, data_inizio, data_fine]):
        return jsonify({"error": "Titolo e date sono obbligatori."}), 400

    query = """
        INSERT INTO evento (titolo, data_inizio, data_fine, id_organizzatore, path_planimetria) 
        VALUES (%s, %s, %s, %s, %s)
    """
    id_nuovo_evento = db.execute_query(query, (titolo, data_inizio, data_fine, get_jwt().get('sub'), path_planimetria))
    
    return jsonify({"message": "Evento creato con successo!", "id_evento": id_nuovo_evento}), 201

# --- 2. GESTIONE UTENTI (Bans e Promozioni) ---

@admin_bp.route('/utenti', methods=['GET'])
@jwt_required()
@ruolo_richiesto('admin')
def get_utenti():
    """Restituisce l'elenco di tutti gli utenti usando il wrapper."""
    try:
        utenti = db.get_utenti_ordinati()
        return jsonify(utenti), 200
    except Exception as e:
        return jsonify({"error": "Errore nel recupero degli utenti."}), 500

@admin_bp.route('/utenti/<id_utente>/ruolo', methods=['PUT'])
@jwt_required()
@ruolo_richiesto('admin')
def modifica_ruolo_utente(id_utente):
    """Promuove o declassa un utente."""
    nuovo_ruolo = request.get_json().get('ruolo')
    if nuovo_ruolo not in ['steward', 'organizzatore', 'admin']:
        return jsonify({"error": "Ruolo non valido."}), 400
        
    query = "UPDATE utente SET ruolo = %s WHERE id_utente = %s"
    db.execute_query(query, (nuovo_ruolo, id_utente))
    return jsonify({"message": f"Ruolo aggiornato a {nuovo_ruolo}."}), 200

# --- 3. DASHBOARD STATISTICHE AVANZATE ---

@admin_bp.route('/dashboard/stats/<int:id_evento>', methods=['GET'])
@jwt_required()
@ruolo_richiesto('organizzatore', 'admin')
def get_statistiche_dashboard(id_evento):
    """
    Recupera le statistiche complesse per un evento specifico: 
    copertura settori, stima ore e rating medio dai report.
    """
    
    # Statistica 1: Rating medio dei report di fine turno
    query_rating = """
        SELECT COALESCE(AVG(r.rating_scorrevolezza), 0) as rating_medio 
        FROM report_fine_turno r
        JOIN turno_assegnato t ON r.id_turno = t.id_turno
        JOIN settore s ON t.id_settore = s.id_settore
        WHERE s.id_evento = %s
    """
    rating = db.fetch_one(query_rating, (id_evento,))
    
    # Statistica 2: Copertura numerica del personale (Confermati vs Richiesti)
    query_copertura = """
        SELECT 
            SUM(capacita_richiesta) as posti_totali,
            (SELECT COUNT(*) FROM turno_assegnato t2 
             JOIN settore s2 ON t2.id_settore = s2.id_settore 
             WHERE s2.id_evento = %s AND t2.stato_candidatura = 'confermato') as steward_confermati
        FROM settore s
        WHERE s.id_evento = %s
    """
    copertura = db.fetch_one(query_copertura, (id_evento, id_evento))
    
    # Riassembliamo i dati per il frontend
    statistiche = {
        "rating_medio": round(float(rating['rating_medio']), 1),
        "posti_totali_richiesti": int(copertura['posti_totali'] or 0),
        "steward_confermati": int(copertura['steward_confermati'] or 0)
    }
    
    return jsonify(statistiche), 200