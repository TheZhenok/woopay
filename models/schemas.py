from marshmallow import (
    Schema,
    validate,
    fields,
)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=[validate.Length(max=250)]
    )
    email = fields.Email()
    iin = fields.String(
        required=True,
        validate=[validate.Length(max=12, min=12)]
    )
    password_hash = fields.String(validate=[validate.Length(max=255, min=6)])
    datetime_created = fields.DateTime(dump_only=True)
    datetime_updated = fields.DateTime(dump_only=True)
    datetime_deleted = fields.DateTime(dump_only=True)


class UserRegisterSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=[validate.Length(max=250)]
    )
    email = fields.Email(required=True)
    password_hash = fields.String(
        required=True,
        validate=[validate.Length(max=255, min=6)
    ])
    datetime_created = fields.DateTime(dump_only=True)
    datetime_updated = fields.DateTime(dump_only=True)
    datetime_deleted = fields.DateTime(dump_only=True)


class CardSchema(Schema):
    id = fields.Integer(dump_only=True)
    owner_id = fields.Integer(required=True)
    number = fields.String(dump_only=True)
    validity_period = fields.Date(dump_only=True)
    cvv = fields.String(dump_only=True)
    balance = fields.Float()
    is_active = fields.Boolean()
    datetime_created = fields.DateTime(dump_only=True)
    datetime_updated = fields.DateTime(dump_only=True)
    datetime_deleted = fields.DateTime(dump_only=True)


class TransactionSchema(Schema):
    id = fields.Integer(dump_only=True)
    card_id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
