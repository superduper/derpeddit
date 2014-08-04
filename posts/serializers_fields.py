from rest_framework.fields import Field


class SubDocumentRelatedField(Field):
    """
    Represents a relationship using a unique field on the target.
    """
    read_only = True

    def __init__(self, *args, **kwargs):
        self.field = kwargs.pop('field', None)
        self.serializer = kwargs.pop('serializer', None)
        self.many = kwargs.pop('many', None)
        assert self.field, 'field is required'
        assert self.serializer, "serializer is required"
        super(SubDocumentRelatedField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        if self.many:
            return self.serializer(obj.all(), many=True).data
        return self.serializer(getattr(obj, self.field)).data

    def from_native(self, data):
        pk = data[self.field]
        cls = self.serializer.opts.model
        return cls.objects.get(pk=pk)


class SubDocumentField(Field):
    """
    Represents a relationship using a unique field on the target.
    """
    read_only = True

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        self.many = kwargs.pop('many', None)
        assert self.serializer, "serializer is required"
        super(SubDocumentField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        if self.many:
            return self.serializer(obj.all(), many=True).data
        return self.serializer(obj).data

    def from_native(self, data):
        cls = self.serializer.opts.model
        return cls.objects.get(pk=data)