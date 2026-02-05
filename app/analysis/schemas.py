from marshmallow import Schema, fields, validate

class BulkCheckSchema(Schema):
    #14. madde birden fazla IP'yi toplu sorgulamak için liste şeması

    ips=fields.List(
        fields.Str(),
        required=True,
        validate=validate.Length(min=1,max=100)
    )