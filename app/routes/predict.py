from flask import Blueprint, jsonify, request
from app.services.predict import predict, predict_by_devices

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/', methods=['GET'])
def get_predict():
    try:
        return jsonify(predict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@predict_bp.route("/by_devices", methods=['POST'])
def get_predict_by_devices():
    try:
        data = request.get_json()
        if 'deviceIds' not in data:
            return jsonify({'error': 'deviceIds is required'}), 400
        if not isinstance(data['deviceIds'], list):
            return jsonify({'error': 'deviceIds must be a list'}), 400
        print(data)
        return jsonify(predict_by_devices(data['deviceIds'], data["time"]))
    except Exception as e:
        return jsonify({'error': str(e)}), 500