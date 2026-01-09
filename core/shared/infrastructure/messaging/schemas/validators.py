# filename : core/shared/infrastructure/messaging/schemas/validators.py
class SchemaValidationError(Exception):
    pass


# class JsonSchemaValidator:
#     REQUIRED_FIELDS = {
#         "event_id": str,
#         "event_type": str,
#         "occurred_at": str,
#         "payload": dict,
#         "version": int,
#         # mayme version_type i also do it somewhere
#     }

#     @classmethod
#     def validate(cls, message: dict):
#         for field, field_type in cls.REQUIRED_FIELDS.items():
#             if field not in message:
#                 raise SchemaValidationError(f"Missing field: {field}")
#             if not isinstance(message[field], field_type):
#                 raise SchemaValidationError(
#                     f"Invalid type for {field}: expected {field_type}"
#                 )


class JsonSchemaValidator:
    REQUIRED_FIELDS = {
        "event_id": str,
        "event_type": str,
        "payload": dict,
        "version": int,
        "metadata": dict,
    }

    METADATA_REQUIRED_FIELDS = {
        "occurred_at": str,
    }

    @classmethod
    def validate(cls, message: dict):
        for field, field_type in cls.REQUIRED_FIELDS.items():
            if field not in message:
                raise SchemaValidationError(f"Missing field: {field}")
            if not isinstance(message[field], field_type):
                raise SchemaValidationError(
                    f"Invalid type for {field}: expected {field_type}"
                )

        metadata = message["metadata"]
        for field, field_type in cls.METADATA_REQUIRED_FIELDS.items():
            if field not in metadata:
                raise SchemaValidationError(f"Missing metadata field: {field}")
            if not isinstance(metadata[field], field_type):
                raise SchemaValidationError(f"Invalid metadata type for {field}")
