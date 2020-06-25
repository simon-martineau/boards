from rest_framework.relations import HyperlinkedIdentityField


# noinspection PyShadowingBuiltins
class ComplexHyperlinkedIdentityField(HyperlinkedIdentityField):
    """HypelinkedRelatedField for complex view lookups"""
    extra_view_kwargs: dict = None

    def __init__(self, view_name=None, **kwargs):
        self.extra_view_kwargs = kwargs.pop('extra_view_kwargs', self.extra_view_kwargs)
        super().__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        extra_kwargs = {}
        if self.extra_view_kwargs:
            for key, attribute in self.extra_view_kwargs.items():
                extra_kwargs[key] = getattr(obj, attribute)

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value, **extra_kwargs}
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
