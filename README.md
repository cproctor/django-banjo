# Banjo

This is a django wrapper which provides a simplified subset of django's
functionality. The intended usage is that students will only interact
with `banjo`, not `django`. All the django documentation can be used for
reference, with the caveat that many of the options are not available.

## Needs

The purpose of Banjo is to introduce databases as a persistence layer behind an
API server, while abstracting away details for which students are not yet ready 
while creating as few misconceptions as possible. 

Banjo should be thought of as scaffolding; when they are ready, students should
be able to seamlessly transition to django.

Specific concepts which we target for simplification include:

- Simplify DB schema: A severly-limited subset of field types is provided.
  There are no foreign key relations or field options. Field names correspond to
  familiar Python types. All fields have default values.

- Simplify filesystem layout: Only two files are required: `models.py` and
  `views.py`. View-URL binding is handled by decorators, as in flask, and all
  URLs are static (there are no placeholders and no params are passed to the
  view). Additionally, `db.sqlite3` will be created when the server runs.

- Simplify management commands: There is a single command, `banjo`, which
  effectively runs django's `makemigrations`, `migrate`, and `runserver` in sequence.
