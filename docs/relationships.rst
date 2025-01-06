.. _relationships:

Relationships between models
============================

You can define relationships between models, and then use those relationships
to build powerful queries. The ``ForeignKey`` field creates a relationship 
from one model to another. For example::

    # app/models.py
    from banjo.models import Model, StringField, ForiegnKey

    class Recipe(Model):
        name = StringField()

    class Ingredient(Model):
        name = StringField()
        recipe = ForeignKey("Recipe")

This is called a "one-to-many" relationship because each ingredient has one
recipe, but each recipe can have many ingredients. You can play with these
models in the shell::

    >>> stew = Recipe(name="stew")
    >>> stew.save()
    >>> meat = Ingredient(name="meat", recipe=stew)
    >>> meat.save()
    >>> carrots = Ingredient(name="carrots", recipe=stew)
    >>> carrots.save()
    >>> meat.recipe
    <Recipe {'ingredient_set': [{'id': 1, 'name': 'meat', 'recipe': 1}, 'id': 1, 'name': 'stew'}>
    >>> stew.ingredient_set.random()
    <Ingredient {'id': 2, 'name': 'carrots', 'recipe': {'id': 1, 'name': 'stew'}}>

Each ``Ingredient`` has a ``recipe`` attribute. Each ``Recipe`` has an attribute
called ``ingredient_set``, which you could query in the same way as a model (e.g. ``first``, 
``filter``, ``all``). You can specify a different name for the reverse relation
by using the ``related_name`` argument::

    class Ingredient(Model):
        name = StringField()
        recipe = ForeignKey("Recipe", related_name="ingredients")


Creating objects with relationships
-----------------------------------

Banjo's models come with a convenient `from_dict` method, commonly used
to create a model instance from params. For example::

    # app/views.py
    from banjo.urls import route_post

    @route_post('recipes/new', args={'name': str})
    def create_recipe(params):
        recipe = Recipe.from_dict(params)
        recipe.save()
        return recipe.to_dict()

When objects require


