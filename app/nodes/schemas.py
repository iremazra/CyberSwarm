#app/nodes/schemas.py
from marshmallow import Schema, fields,validate

class NodeSchema(Schema):
    """Genel Node verisi gösterim şeması"""
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    node_type = fields.Str(validate=validate.OneOf(['server', 'sensor']))
    status = fields.Str(dump_only=True)
    reputation_score = fields.Float(dump_only=True)
    last_seen = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    organization_id = fields.UUID(dump_only=True)
    api_key=fields.Str(required=True)

    organization_name=fields.Method("get_organization_name", dump_only=True)

    def get_organization_name(self, obj):
        #obje bir tuple gelirse hata vermemesi için kontrol ekliyoruz
        if isinstance(obj, tuple):
            obj = obj[0]
        if obj and hasattr(obj, 'organization_obj') and obj.organization_obj:
            return obj.organization_obj.name
        return "CyberSwarm Default"

class NodeRegisterSchema(Schema):
    """Yeni düğüm kaydı için gereken veriler"""
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    # Tip belirtilmezse sensor olarak kabul edebiliriz
    node_type = fields.Str(required=False, load_default='sensor', validate=validate.OneOf(['server', 'sensor']))

class HeartbeatSchema(Schema):
    """Heartbeat endpoint'i için gereken veri"""
    node_id = fields.UUID(required=True)