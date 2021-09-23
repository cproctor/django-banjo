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
  familiar Python types. All fields have default values. Within these
  constraints, django's full ORM is available.

- Simplify filesystem layout: Only two files are required: `models.py` and
  `views.py`. View-URL binding is handled by decorators, as in flask, and all
  URLs are static (there are no placeholders and no params are passed to the
  view). Additionally, `db.sqlite3` will be created when the server runs.

- Simplify management commands: There is a single command, `banjo`, which
  effectively runs django's `makemigrations`, `migrate`, and `runserver` in sequence.

- Simplify request/response lifecycle: View functions receive a status code and
  a dict of POST params. View functions must return a dict. Http errors
  are provided as exceptions, which simplifies control flow. 
  Models have helper methods, `from_dict` and `to_dict`. 

## Usage

To write a Banjo app, you define models in `models.py` and define views in
`views.py`. Here's a simple example:

### `models.py`

    from banjo.models import Model, StringField

    class Animal(Model):
        name = StringField()
        sound = StringField()
    
### `views`

    from banjo.urls import route
    from models import Animal
    
    @route('newanimal')
    def add_animal(params):
        animal = Animal.from_dict(params)
        animal.save()
        return animal.to_dict()

    @route('listen')
    def list_animal_noises(params):
        sounds = []
        for animal in Animal.objects.all():
            sounds.append('{} says {}'.format(a.name, a.sound))     
        return {'sounds': sounds}

Now you can run `banjo` from the directory containing these files and the server
will start. `--port` and `--log` are provided as options for using a custom port
and saving logs to a file respectively. 

Here is an example of interacting with this app using the `httpie` command-line
utility:

    $ http localhost:5000/add name=elehpant sound=pffffftttttt

    { 
      "name": "elephant",
      "sound": "pffffftttttt"
    }

    $ http localhost:5000/add name=squirrel sound=chcheee

    { 
      "name": "squirrel",
      "sound": "chcheee"
    }

    $ http localhost:5000/listen

    {
      "sounds": [
        "elephant says pffffftttttt",
        "squirrel says chcheee"
      ]
    }

