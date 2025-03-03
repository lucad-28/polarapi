from flask import Blueprint, jsonify
from app.services.predict import predict

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/', methods=['GET'])
def get_predict():
    try:
        return jsonify(predict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500