import json
from django.db.models import JSONField

from translatable_fields.value import TranslatableValue


class TranslatableField(JSONField):
    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return value

        instance = TranslatableValue()
        instance.update(json.loads(value))

        return instance

    def to_python(self, value):
        if isinstance(value, TranslatableValue):
            return value

        if value is None:
            return value

        instance = TranslatableValue()
        instance.update(value)

        return instance
