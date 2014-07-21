import inspect
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.validators import validate_slug


class SerializerRelatedField(serializers.SlugRelatedField):
    """
    SerializerRelatedField for DjangoRestFramework

    for data add: Slug   @from_native
    for data list or detail: serializer   @to_native

    Example:
    SerializerRelatedField(serializer_field=TagsSerializer,
                           slug_field='slug')
    """

    def __init__(self, *args, **kwargs):
        self.serializer_field = kwargs.pop('serializer_field', None)
        assert self.serializer_field, 'serializer_field is required'
        assert inspect.isclass(self.serializer_field)
        super(SerializerRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        # list or detail
        return self.serializer_field(instance=obj).data


class GetOrCreateField(SerializerRelatedField):
    """
    Get Or Create Field

    Example:
    GetOrCreateField(serializer_field=TagsSerializer, slug_field='slug')
    """

    def from_native(self, data):
        if self.queryset is None:
            raise Exception('Writable related fields must include a '
                            '`queryset` argument')
        try:
            data = data.strip().lower()
            validate_slug(data)
            obj, _ = self.queryset.get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise ValidationError(msg)
