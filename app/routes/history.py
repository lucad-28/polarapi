from flask import Blueprint, jsonify, request
from app.services.history import get_resampled_history, update_history, get_history_by_devicesIds, get_resampled_history_by_devicesIds

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
def history():
    try:
        return jsonify(get_resampled_history())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@history_bp.route("/by_devices", methods=['POST'])
def history_by_devices():
    try:
        data = request.get_json()
        if 'deviceIds' not in data:
            return jsonify({'error': 'deviceIds is required'}), 400
        if not isinstance(data['deviceIds'], list):
            return jsonify({'error': 'deviceIds must be a list'}), 400
        
        return jsonify(get_history_by_devicesIds(data['deviceIds']))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/resampled', methods=['GET'])
def resampled():
    try:
        return jsonify(get_resampled_history())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@history_bp.route("/resampled/by_devices", methods=['POST'])
def resampled_by_devices():
    try:
        data = request.get_json()
        if 'deviceIds' not in data:
            return jsonify({'error': 'deviceIds is required'}), 400
        if not isinstance(data['deviceIds'], list):
            return jsonify({'error': 'deviceIds must be a list'}), 400
        
        return jsonify(get_resampled_history_by_devicesIds(data['deviceIds']))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        return jsonify(update_history(data['deviceId']))
    except Exception as e:
        return jsonify({'error': str(e)}), 500