Debugging
=========

Issues with migrations
----------------------

When you change a model Banjo creates a migration, or a representation of the change
which allows the structure of the database (its schema) to be updated as well as
existing records. In most cases, existing records can be automatically updated. For 
example, if you add a new ``IntegerField``, all the existing records will be assigned
the most sensible default value, ``0``.

However, there are some situations where there is no simple way to update existing 
records. For example, if you add a ``ForeignKey`` field to a model, what value
should be assigned to existing records? In this situation, you are likely to see 
something line this::

    It is impossible to add a non-nullable field 'recipe' to ingredient without specifying a default. This is because the database needs something to populate existing rows.
    Please select a fix:
    1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
    2) Quit and manually define a default value in models.py.

You could enter ``1`` and provide the id of an existing record. Or you could use a simple
if brutal approach: destroy the database and rebuild it from scratch by running::

    banjo --clean

This will delete all existing data in the database.
