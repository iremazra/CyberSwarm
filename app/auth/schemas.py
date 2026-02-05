# app/auth/schemas.py
from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    name= fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True,validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))
    organization_name= fields.Str(required=True, validate=validate.Length(min=3, max=100))
  
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UpdateProfileSchema(Schema):
    name= fields.Str(validate=validate.Length(min=3, max=50))
    email = fields.Email(validate=validate.Email())
    password = fields.Str(validate=validate.Length(min=6))
    notification_preferences = fields.Dict(keys=fields.Str(), values=fields.Bool())

class AdminRegisterSchema(Schema):
    email = fields.Email(required=True,validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))
    name=fields.Str(required=True, validate=validate.Length(min=3, max=50))