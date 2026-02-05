from marshmallow import Schema, fields, validate,pre_load,ValidationError
import ipaddress


def validate_ip(ip_str):
    """IP adresinin gerçek bir IPv4 veya IPv6 olduğunu doğrular."""
    try:
        ipaddress.ip_address(ip_str)
    except ValueError:
        raise ValidationError("It's not a valid IP adress")
    
class ThreatReportSchema(Schema):
    #11. madde: sensörlerin saldırı bildirmesi için şema
    #Beklenen veri: IP, timestamp, attack_vector

    attacker_ip = fields.Str(required=True, validate=validate_ip)
    

    attack_vector = fields.Str(required=True, validate=validate.OneOf(
        ["ddos_tcp", "udp_flood", "http_flood","syn_flood","icmp_flood"],
        error ="Invalid attack vector. Must be one of the predefined types: ddos_tcp, udp_flood, http_flood,syn_flood,icmp_flood")
    )

    timestamp = fields.DateTime(required=False) # Sensör saati göndermezse sunucu saati kullanılır.

    @pre_load
    def process_attack_vector(self,data,**kwargs):
        if data and 'attack_vector' in data:
            val= str(data['attack_vector']).lower().strip()
            # Türkçe 'ı' karakterini standart 'i'ye çevirerek riskleri sıfırlıyoruz
            data['attack_vector'] = val.replace('ı', 'i')
        return data

class IPScoreSchema(Schema):
    #12. madde bir IP'nin itibar skorunu döndüren şema

    attacker_ip=fields.Str(dump_only=True)
    reputation_score=fields.Float(dump_only=True)
    total_reports=fields.Int(dump_only=True)
    last_attack_at=fields.DateTime(dump_only=True)



