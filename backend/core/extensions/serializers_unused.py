from typing import Any, Union, Tuple, List

from rest_framework.serializers import ModelSerializer

from core.extensions.relations_unused import ComplexHyperlinkedIdentityField


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class HyperlinkAndFieldsModelSerializer(DynamicFieldsModelSerializer):
    """Serializer to output specific fields as well as a uri"""
    href = None

    def __init__(self, href_field_kwargs: dict = None, *args, **kwargs):
        assert href_field_kwargs is not None and isinstance(href_field_kwargs, dict), 'href_field_kwargs needs to be' \
                                                                                      ' a defined dictionary'
        default_href_field_kwargs = {
            'read_only': True
        }
        default_href_field_kwargs.update(href_field_kwargs)

        self.href = ComplexHyperlinkedIdentityField(**default_href_field_kwargs)

        fields = kwargs.pop('fields')
        fields = _ensure_in_array(fields, 'href')
        kwargs['fields'] = fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = '__all__'


def _ensure_in_array(container: Union[Tuple, List], value: Any) -> List:
    if value not in container:
        return [value] + list(container)
