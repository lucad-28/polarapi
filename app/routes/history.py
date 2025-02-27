from flask import Blueprint, jsonify
from app.services.history import get_resampled_history, get_history

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
def history():
    try:
        return jsonify(get_history())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/resampled', methods=['GET'])
def resampled():
    try:
        return jsonify(get_resampled_history())
    except Exception as e:
        return jsonify({'error': str(e)}), 500