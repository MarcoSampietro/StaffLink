from flask import Blueprint, jsonify, request
from DatabaseWrapper import DatabaseWrapper
from auth import require_auth

turni_bp = Blueprint('turni', __name__)

@turni_bp.route('/disponibili', methods=['GET', 'OPTIONS'])
@require_auth
def disponibili():
    if request.method == "OPTIONS": return jsonify({}), 200
    return jsonify([]), 200
