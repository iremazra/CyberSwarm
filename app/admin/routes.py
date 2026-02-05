from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.auth.utils import token_Required, role_required
from .service import add_to_whitelist, remove_from_whitelist,get_admin_global_stats
from .schemas import WhiteListSchema, AuditLogSchema, GlobalAdminStatsSchema
from .models import AuditLog, WhitelistIP
from . import admin_bp

#16. madde: whitelist (post)
@admin_bp.route('/whitelist',methods=["POST"])
@token_Required
@role_required('admin')
def api_add_whitelist():
   
   try:
      data=WhiteListSchema().load(request.get_json())
      result=add_to_whitelist(
         data.get("ip_address"),
         data.get("reason","Internal Trusted IP"),
         request.user["sub"])

      return jsonify({
         "status":"success",
         "data":WhiteListSchema().dump(result)
      }),201
   except ValidationError as err:
      return jsonify({"status": "error", "errors": err.messages}), 400
   except ValueError as e:
      return jsonify({
          "status": "error", 
          "message": str(e) # "IP 8.8.8.8 is already whitelisted." mesajı döner
      }), 409 # 409 Conflict: Bir kaynağın zaten var olduğunu belirtmek için en doğru koddur

#artıdan eklenen madde
@admin_bp.route('/whitelist/<string:ip_address>', methods=["DELETE"])
@token_Required
@role_required("admin")
def api_remove_whitelist(ip_address):
   try:
      remove_from_whitelist(ip_address,request.user["sub"])

      return jsonify({
         "status":"success",
         "message":f"IP {ip_address} has been removed from whitelist and is now being monitored again"
      }),200
   except ValueError as err:
      return jsonify({
         "status":"error",
         "message":str(err)
      }),404 #Bulunamadı hatası

#17.madde:Global Stats (Get)
@admin_bp.route('/stats_global',methods=['GET'])
@token_Required
@role_required('admin')
def api_global_stats():
   stats=get_admin_global_stats()
   return jsonify(GlobalAdminStatsSchema().dump(stats)),200

#18.madde : AuditLogs
@admin_bp.route('/audit_logs',methods=['GET'])
@token_Required
@role_required('admin')
def api_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    # 4. many=True kullanarak liste halindeki logları dön
    return jsonify(AuditLogSchema(many=True).dump(logs)), 200

#19.madde: Monitoring whitelists
@admin_bp.route('/whitelist_monitoring',methods=['GET'])
@token_Required
@role_required('admin')
def whitelist_monitoring():
   list = WhitelistIP.query.order_by(WhitelistIP.added_at.desc()).all()
   return jsonify(WhiteListSchema(many=True).dump(list)), 200