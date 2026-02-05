#app/nodes/routes.py
from flask import Blueprint,request, jsonify
from app.auth.utils import token_Required, role_required
from .service import register_node, get_nodes_by_organization, process_heartbeat,delete_node, get_nodes_by_role,get_node_by_id
from .schemas import NodeRegisterSchema, HeartbeatSchema,NodeSchema
from marshmallow import ValidationError
from . import nodes_bp



@nodes_bp.route('/register', methods=['POST'])
@token_Required
@role_required('user') # Sadece 'user' rolündeki kişiler düğüm ekleyebilir
def register():
    try:
        raw_data=request.get_json()
        validated_data=NodeRegisterSchema().load(raw_data) #veriyi schemas ile doğruluyoruz
        
        #Token'dan organizasyon kimliğini al
        org_id=request.user.get("organization_id")
        if not org_id:
            return jsonify({"error": "Organization ID not found in token"}), 401
        
        node=register_node(org_id,validated_data)
        result=NodeSchema().dump(node)
        result['api_key']=node.api_key  #API anahtarını yanıt verisine ekle
        return jsonify(result), 201
        
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    

@nodes_bp.route('/list', methods=['GET'])
@token_Required
def list_nodes():
    try: #ORganizasyona ait tüm aktif sensör düğümleri listelenir.
        #Token'dan organizasyon kimliğini al
        user_role=request.user.get("role")
        org_id=request.user.get('organization_id')
        if not org_id:
            return jsonify({"error": "Organization ID not found in token"}), 401
        
        nodes=get_nodes_by_role(user_role,org_id)
        return jsonify(NodeSchema(many=True).dump(nodes)), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

@nodes_bp.route('/<uuid:id>', methods=['GET', 'DELETE'])
@token_Required
def handle_node(id): #Belirlli bir düğümün detaylarını getirir veya siler
    org_id=request.user.get('organization_id')
    role=request.user.get('role')
    if request.method=='GET':
        try:
            node=get_node_by_id(id,org_id,role)
            if not node:
                return jsonify({"error": "Node not found"}), 404
            return jsonify(NodeSchema().dump(node)), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
    
    elif request.method=='DELETE':
        if delete_node(id,org_id):
            return jsonify({"message": "Node deleted successfully"}), 200
        return jsonify({"error": "Node not found or could not be deleted"}), 404
    
@nodes_bp.route('/heartbeat', methods=['POST']) #Sensör düğümünden kalp atış sinyali alır
def heartbeat():
    try:
        raw_data=request.get_json()
        validation_data=HeartbeatSchema().load(raw_data)
        node_id=validation_data.get('node_id')

        success=process_heartbeat(node_id)
        if not node_id:
            return jsonify({"error": "Node ID is required"}), 400
        if success:
            return jsonify({
                "status": "success",
                "message": "Heartbeat received"}), 200
        else:
            return jsonify({"error": "Node not found"}), 404
        
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400