Teaching with Banjo
-------------------

The purpose of Banjo is to introduce databases as a persistence layer
behind an API server, while abstracting away details for which students
are not yet ready and creating as few misconceptions as possible. Banjo
should be thought of as scaffolding; when they are ready, students
should be able to seamlessly transition to Django.

Specific concepts which we target for simplification include:

-  Simplify DB schema: A severely-limited subset of field types is
   provided. Field names correspond to familiar Python types. All fields
   have default values. Migrations are handled automatically. Within
   these constraints, Django’s full ORM is available.
-  Simplify filesystem layout: Only two files are required:
   ``models.py`` and ``views.py``.
-  Simplify management commands: There is a single command, ``banjo``,
   which effectively runs Django’s ``makemigrations``, ``migrate``, and
   ``runserver`` in sequence. ``banjo --shell`` enters the REPL with all
   user-defined models loaded.
-  Simplify request/response lifecycle: View functions receive a dict of
   params and must return a dict. View-URL binding is handled by
   decorators, as in flask, and all URLs are static (there are no
   placeholders and no params are passed to the view). Http errors are
   provided as exceptions, which simplifies control flow. Models have
   ``from_dict`` (class method) and ``to_dict`` (instance method)
   helpers.

Banjo was designed for use by teachers familiar with Django; this is
intentionally a leaky abstraction which provides a structured
introduction into the power and the complexity of the underlying system.
