from django.db import models
from django.db.models import Field, ForeignKey, ManyToOneRel
from random import choice, sample

class RandomItemQuerySet(models.QuerySet):
    """Extends the base QuerySey with random() and sample() methods
    """
    def random(self):
        ids = self.values_list('id', flat=True)
        if not ids:
            raise self.model.DoesNotExist(f"{self.model.__name__} is empty")
        return self.get(id=choice(ids))

    def sample(self, n):
        ids = self.values_list('id', flat=True)
        if len(ids) < n:
            raise self.model.DoesNotExist(f"Requested {n} but {self.model.__name__} only contains {len(ids)} objects.")
        return self.filter(id__in=sample([i for i in ids], n))

def serialize(obj):
    """Safely converts an object to a dict, 
    regardless of whether it implements banjo's `to_dict` interface.
    """
    if hasattr(obj, 'to_dict'):
        try:
            return obj.to_dict(with_related=False)
        except TypeError:
            return obj.to_dict()
    else:
        return {'id': obj.id}

class Model(models.Model):

    objects = models.Manager.from_queryset(RandomItemQuerySet)()

    @classmethod
    def from_dict(cls, props):
        """Tries to create an instance of Model from props.
        """
        if 'id' in props:
            del props['id']
        return cls(**props)

    def to_dict(self, with_related=True):
        """Returns a json representation of the Model.
        """
        d = {}
        for field in self._meta.get_fields():
            if with_related and isinstance(field, ForeignKey):
                related_object = getattr(self, field.name)
                d[field.name] = serialize(related_object)
            elif isinstance(field, Field):
                d[field.name] = field.value_from_object(self)
            elif with_related and isinstance(field, ManyToOneRel):
                related_objects = getattr(self, field.get_accessor_name()).all()
                d[field.get_accessor_name()] = [serialize(obj) for obj in related_objects]
        return d

    def __str__(self):
        return "<{} {}>".format(self.__class__.__name__, self.to_dict())

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True
        app_label = "app"

class BooleanField(models.BooleanField):
    """A database column which stores a boolean.
    The default value is False.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = False
        models.BooleanField.__init__(self, *args, **kwargs)

class IntegerField(models.IntegerField):
    """A database column which stores an integer.
    The default value is 0.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0
        models.IntegerField.__init__(self, *args, **kwargs)

class FloatField(models.FloatField):
    """A database column which stores a float.
    The default value is 0.0.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0.0
        models.FloatField.__init__(self, *args, **kwargs)

class StringField(models.TextField):
    """A database column which stores a string.
    The default value is '', the empty string.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = ''
        models.TextField.__init__(self, *args, **kwargs)

class ForeignKey(models.ForeignKey):
    """A database column which links a model to another model.
    """
    def __init__(self, *args, **kwargs):
        kwargs['on_delete'] = models.CASCADE
        models.ForeignKey.__init__(self, *args, **kwargs)
