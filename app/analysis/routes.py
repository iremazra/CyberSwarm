from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.auth.utils import token_Required
from .schemas import BulkCheckSchema
from .service import perform_bulk_analysis
from app.threats.schemas import IPScoreSchema
from . import analysis_bp


#14.madde: Bulk-check
@analysis_bp.route('/bulk-check',methods=['POST'])
@token_Required
def bulk_check():
    try:
        raw_data=request.get_json()
        validated_data=BulkCheckSchema().load(raw_data)

        results=perform_bulk_analysis(validated_data['ips'])

        return jsonify({
            "status":"success",
            "results":IPScoreSchema(many=True).dump(results)
        }),200
    except ValidationError as err:
        return jsonify({"error":err.messages}),400





