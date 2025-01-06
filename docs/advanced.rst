Using Django features
=====================

Once you are comfortable with Banjo, you may find yourself wanting to do 
something that isn't supported by Banjo. Fortunately, Banjo is just a 
simplified wrapper around `Django <https://www.djangoproject.com/>`_, 
a full-powered web application framework which has excellent documentation. 

If you are willing to learn some new concepts, you can import features from Django
into a Banjo project. Banjo's model and field classes already support many 
Django features we have not previously discussed. For example, if you wanted to 
make sure that a model field never has duplicate values, you could use the 
`unique <https://docs.djangoproject.com/en/5.1/ref/models/fields/#unique>`_ 
argument when you define the field.

In other cases, you can import classes from Django into a Banjo project. 
For example, if you wanted to create an app which works with 
dates, you might want to include a 
`date field <https://docs.djangoproject.com/en/5.1/ref/models/fields/#datefield>`_. 
For example::

    # app/models.py

    from banjo.models import Model, StringField
    from django.db.models import DateField

    class Birthday(Model):
        name = StringField()
        birthday = Date()

Of course then you have to learn how to work with 
`dates <https://docs.python.org/3/library/datetime.html#date-objects>`_.

Banjo can take you a long way. Hopefully as you grow you will find yourself
using more and more functionality from Django, until at some point you have 
outgrown Banjo entirely and are creating and deploying full-powered web 
applications. 

