from marshmallow import Schema, fields, validate

class UserPublicSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    role = fields.Str()

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(allow_none=True)
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
