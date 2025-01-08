More about models
=================

This section goes into more detail on how to work with models. You can read much more
in `Django's documentation on models <https://docs.djangoproject.com/en/5.1/topics/db/models/>`_.

In the examples below, we will work with two simple models: ``Recipe`` and ``Ingredient``::

    # app/models.py
    from banjo.models import Model, StringField, ForeignKey

    class Recipe(Model):
        name = StringField()

    class Ingredient(Model):
        name = StringField()
        recipe = ForeignKey("Recipe")

In this example, we define a relationship between recipes and ingredients using a
``ForeignKey``. This is called a "one-to-many" relationship because each ingredient has one
recipe, but each recipe can have many ingredients.

Each ``Ingredient`` has a ``recipe`` attribute. Each ``Recipe`` has an attribute
called ``ingredient_set``, which you could query in the same way as a model (e.g. ``first``, 
``filter``, ``all``). You can specify a different name for the reverse relation
by using the ``related_name`` argument::

    class Ingredient(Model):
        name = StringField()
        recipe = ForeignKey("Recipe", related_name="ingredients")

If you want to follow along with these examples, save the code above in `app/models.py`, 
and create an empty `app/views.py` file. Then run::

    banjo --shell

Creating records
----------------

A record is an instance of a model class which is saved in the database. To create a record, 
create a model instance and save it::

    >>> soup = Recipe(name="soup")
    >>> soup.save()
    >>> Ingredient(name="onions", recipe=soup).save()
    >>> Ingredient(name="potatoes", recipe=soup).save()
    >>> Ingredient(name="parsley", recipe=soup).save()

Once you save a model instance, it will have an id::

    >>> soup.id
    1

Queries
-------

Once you have created records, you can use queries to select one or more of them.

Get all records::

    >>> Recipe.objects.all()
    >>> <QuerySet [<Recipe {'ingredients': [{'id': 1, 'name': 'onions', 'recipe': 1}, {'id': 2, 'name': 'potatoes', 'recipe': 1}, {'id': 3, 'name': 'parsley', 'recipe': 1}], 'id': 1, 'name': 'soup'}>]>

Get one record::

    >>> Ingredient.objects.first()
    <Ingredient {'id': 1, 'name': 'onions', 'recipe': {'id': 1, 'name': 'soup'}}>
    >>> Ingredient.objects.last()
    <Ingredient {'id': 3, 'name': 'parsley', 'recipe': {'id': 1, 'name': 'soup'}}>
    >>> Ingredient.objects.random()
    <Ingredient {'id': 2, 'name': 'potatoes', 'recipe': {'id': 1, 'name': 'soup'}}>

Get a specific record. This will raise an error if no matching record exists
(``Recipe.DoesNotExist``) or if more than one record matches (``Recipe.MultipleObjectsReturned``)::

    >>> Ingredient.objects.get(name="potatoes")
    <Ingredient {'id': 2, 'name': 'potatoes', 'recipe': {'id': 1, 'name': 'soup'}}>
    >>> Ingredient.objects.get(id=1)
    <Ingredient {'id': 1, 'name': 'onions', 'recipe': {'id': 1, 'name': 'soup'}}>

Filter records based on conditions (Read more at `Django's documentation on queries <https://docs.djangoproject.com/en/5.1/topics/db/queries/>`_)::

    >>> Ingredient.objects.filter(name__startswith="p") # All ingredients whose name starts with p.
    <QuerySet [<Ingredient {'id': 2, 'name': 'potatoes', 'recipe': {'id': 1, 'name': 'soup'}}>, <Ingredient {'id': 3, 'name': 'parsley', 'recipe': {'id': 1, 'name': 'soup'}}>]>
    >>> Ingredient.objects.filter(id__gt=2) # All ingredients whose id is greater than 2.
    <QuerySet [<Ingredient {'id': 3, 'name': 'parsley', 'recipe': {'id': 1, 'name': 'soup'}}>]>
    >>> Recipe.objects.filter(ingredient__name="vinegar") # All recipes which have an ingredient named vinegar.

Sometimes you don't need all the results, you just need to know how many there are, or whether any exist at all::

    >>> Ingredient.objects.filter(name__contains="o").count() # How many ingredients have o in their name?
    2
    >>> Ingredient.objects.filter(recipe__name="bread").exists() # Do any ingredients belong to a recipe named bread?
    False

Changing records
----------------

You can change a record by getting its model instance, changing attributes, and then saving it::

    >>> onion = Ingredient.objects.get(name="onion")
    >>> onion.name = "red onion"
    >>> onion.save()

Deleting records
----------------

You can delete a record by getting its model instance and calling its ``delete`` method. 
If you delete a record, any related records whose ``ForeignKey`` points to the record
will also be deleted. The following will delete your recipe and all its ingredients::

    >>> Recipe.objects.first().delete()
    >>> recipe.objects.exists()
    False

Models and dicts
----------------
Banjo's views are functions which receive a dict and return a dict, so Banjo's models come
with two handy built-in methods: ``from_dict`` and ``to_dict``. You can use ``from_dict``
to create a model instance from a dict::

    >>> Recipe.from_dict({"name": "pizza"})

Models which have relationships can't be created using ``from_dict``.
In the other direction, you can use ``to_dict`` to represent a model instance as a dict::

    >>> Recipe.objects.first().to_dict()
    {'ingredients': [{'id': 1, 'name': 'onions', 'recipe': 1}, {'id': 2, 'name': 'potatoes', 'recipe': 1}, {'id': 3, 'name': 'parsley', 'recipe': 1}], 'id': 1, 'name': 'soup'}

Related objects are also included in the model's dict, which is often convenient.
If you want a different dict representation for a model, simply write your own ``to_dict``
method. 

Options for model fields
------------------------
Here are a few useful options for defining model fields: 

- ``null=True`` makes this value optional. 
- ``unique=True`` will ensure that no two records have the same value for this field.

`Django's documentation <https://docs.djangoproject.com/en/5.1/ref/models/fields/#common-model-field-options>`_
describes many more model field options.
