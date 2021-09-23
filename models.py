# banjo.db.models
# Database models which wrap django
from django.db import models

class Model(models.Model):
    pass

class BooleanField(models.BooleanField):
    """A database column which stores a boolean.
    The default value is False.
    """
    def __init__(self):
        super().__init__(self, default=False)

class IntegerField(models.IntegerField):
    """A database column which stores an integer.
    The default value is 0.
    """
    def __init__(self):
        super().__init__(self, default=0)

class FloatField(models.FloatField):
    """A database column which stores a float.
    The default value is 0.0.
    """
    def __init__(self):
        super().__init__(self, default=0.0)

class StringField(models.TextField):
    """A database column which stores a string.
    The default value is '', the empty string.
    """
    def __init__(self):
        super().__init__(self, default=False)

class DateTimeField(models.DateTimeField):
    """A database column which stores a datetime.
    The default value is datetime.now(), the current time when 
    the model object is created.
    """
    def __init__(self):
        super().__init__(self, default=False)
