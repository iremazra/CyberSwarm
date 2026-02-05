from marshmallow import Schema, validate, fields,ValidationError
import ipaddress

def validate_ip(ip_str):
    """IP adresinin gerçek bir IPv4 veya IPv6 olduğunu doğrular."""
    try:
        ipaddress.ip_address(ip_str)
    except ValueError:
        raise ValidationError("It's not a valid IP adress")

class WhiteListSchema(Schema):
    #16. madde: Güvenilir Ip ekleme şeması
    ip_address=fields.Str(required=True,validate=validate_ip)
    reason=fields.Str(required=False)
    added_at=fields.DateTime(dump_only=True)

class AuditLogSchema(Schema):
    #18. madde: sistem denetim kayıtlarını dönme şeması
    id=fields.UUID(dump_only=True)
    admin_id=fields.UUID(dump_only=True)

    admin_name=fields.Function(lambda obj: obj.admin.name if obj.admin else "Unknown")
    admin_email = fields.Function(lambda obj: obj.admin.email if obj.admin else "Unknown")

    action=fields.Str(dump_only=True)
    target=fields.Str(dump_only=True)
    timestamp=fields.DateTime(dump_only=True)

class GlobalAdminStatsSchema(Schema):
    #17. madde: admin paneli istatistik şeması
    total_threat_logs=fields.Int()
    total_whitelisted_ips=fields.Int()
    vectors=fields.Dict(keys=fields.Str(),values=fields.Int())

