from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.auth.utils import token_Required, user_or_node_required
from app.nodes.models import Node
from .service import calculate_ip_reputation,create_threat_report,get_high_risk_blocklist
from .schemas import ThreatReportSchema, IPScoreSchema
from . import threats_bp

#11. madde :Report threat (sensor only)
@threats_bp.route('/report',methods=['POST'])
def report():
    #Sensörlerden gelen saldırı loglarını kabul eder
    #SENSOR ONLY !! GÜVENLİK--> HEADER'DAN X-API-KEY KONTROLÜ

    api_key=request.headers.get('X-API-KEY')
    node=Node.query.filter_by(api_key=api_key).first()

    if not node:
        return jsonify({"Error:Invalid API Key"}),401
    
    try:
        raw_data=request.get_json()
        validated_date=ThreatReportSchema().load(raw_data)

        report_obj=create_threat_report(node.id,validated_date)
        return jsonify ({ "status":"success"," message":"Attack report processed"}),201
    
    except ValidationError as err:
        return jsonify ({"error": err.messages}),400
    

#12. madde: Get Ip Score
@threats_bp.route('/<string:ip>/score',methods=['GET'])
@token_Required
def get_ip_score(ip):
    #Belirli bir IP'nin itibar skorunu döner.
    result=calculate_ip_reputation(ip)
    return jsonify (IPScoreSchema().dump(result)),200

@threats_bp.route('/feed/blocklist',methods=['GET'])
@user_or_node_required
def get_blocklist():
    high_risk_ips=get_high_risk_blocklist()
    return jsonify({"blocklist":high_risk_ips}),200

@threats_bp.route('/types', methods=['GET'])
def list_attack_types():

    #15. madde: Sistemin tanıyıp analiz edebildiği saldırı tiplerini döner. 
    #[public]
    supported_vectors=[
        "ddos_tcp", 
        "udp_flood", 
        "http_flood", 
        "syn_flood", 
        "icmp_flood"
    ]

    return jsonify({
        "status":"success",
        "attack_vector":supported_vectors,
        "total":len(supported_vectors)
    }),200