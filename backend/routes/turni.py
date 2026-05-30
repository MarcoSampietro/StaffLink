from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from DatabaseWrapper import DatabaseWrapper
from utils.tasks import invia_email_convocazione_async
from . import turni_bp

db = DatabaseWrapper()

@turni_bp.route('/disponibili', methods=['GET'])
@jwt_required()
def get_turni_disponibili():
    """Restituisce gli eventi futuri e i relativi settori."""
    query = """
        SELECT e.id_evento, e.titolo, e.data_inizio, s.id_settore, s.nome_settore, s.capacita_richiesta
        FROM evento e
        JOIN settore s ON e.id_evento = s.id_evento
        WHERE e.data_inizio > NOW()
        ORDER BY e.data_inizio ASC
    """
    eventi = db.fetch_all(query)
    return jsonify(eventi), 200

@turni_bp.route('/candidati', methods=['POST'])
@jwt_required()
def candidati_turno():
    """Permette a uno steward di candidarsi per un settore."""
    dati = request.get_json()
    id_settore = dati.get('id_settore')
    id_steward = get_jwt().get('sub')
    email_steward = get_jwt().get('email')

    if not id_settore:
        return jsonify({"error": "id_settore mancante."}), 400

    # 1. Verifichiamo se è già candidato a questo settore
    check_query = "SELECT id_turno FROM turno_assegnato WHERE id_settore = %s AND id_steward = %s"
    if db.fetch_one(check_query, (id_settore, id_steward)):
        return jsonify({"error": "Ti sei già candidato per questo settore."}), 400

    # 2. Controllo disponibilità in tempo reale
    posti_rimasti = db.check_disponibilita_settore(id_settore)
    
    if posti_rimasti > 0:
        # C'è posto, confermiamo subito
        query = "INSERT INTO turno_assegnato (id_settore, id_steward, stato_candidatura) VALUES (%s, %s, 'confermato')"
        db.execute_query(query, (id_settore, id_steward))
        
        # Recuperiamo info per l'email
        settore_info = db.fetch_one("SELECT e.titolo, s.nome_settore FROM settore s JOIN evento e ON s.id_evento = e.id_evento WHERE s.id_settore = %s", (id_settore,))
        
        # Lanciamo il task asincrono!
        invia_email_convocazione_async(email_steward, settore_info['titolo'], settore_info['nome_settore'])
        
        return jsonify({"message": "Candidatura confermata! Email di riepilogo in arrivo.", "status": "confermato"}), 201
    else:
        # Non c'è posto, finisce in lista d'attesa
        query = "INSERT INTO turno_assegnato (id_settore, id_steward, stato_candidatura) VALUES (%s, %s, 'in_attesa')"
        db.execute_query(query, (id_settore, id_steward))
        return jsonify({"message": "Settore pieno. Inserito in lista d'attesa.", "status": "in_attesa"}), 201

@turni_bp.route('/report', methods=['POST'])
@jwt_required()
def invia_report():
    """Invia il report a fine turno."""
    dati = request.get_json()
    id_turno = dati.get('id_turno')
    rating = dati.get('rating_scorrevolezza')
    commento = dati.get('commento_criticita', '')
    id_steward = get_jwt().get('sub')

    if not all([id_turno, rating]) or not (1 <= int(rating) <= 5):
        return jsonify({"error": "Dati invalidi. Il rating deve essere tra 1 e 5."}), 400

    # Verifica che il turno appartenga a chi sta facendo la richiesta
    verifica_turno = db.fetch_one("SELECT id_steward FROM turno_assegnato WHERE id_turno = %s", (id_turno,))
    if not verifica_turno or verifica_turno['id_steward'] != id_steward:
        return jsonify({"error": "Azione non autorizzata su questo turno."}), 403

    try:
        query = "INSERT INTO report_fine_turno (id_turno, rating_scorrevolezza, commento_criticita) VALUES (%s, %s, %s)"
        db.execute_query(query, (id_turno, rating, commento))
        return jsonify({"message": "Report inviato con successo!"}), 201
    except Exception as e:
        return jsonify({"error": "Report già inviato per questo turno."}), 400