# Banjo

Banjo is an abstraction over django which provides a simplified subset of django's
functionality. All the django documentation can be used for
reference, and many django patterns are replicated here.

## Needs

The purpose of Banjo is to introduce databases as a persistence layer behind an
API server, while abstracting away details for which students are not yet ready 
and creating as few misconceptions as possible. 
Banjo should be thought of as scaffolding; when they are ready, students should
be able to seamlessly transition to django.

Specific concepts which we target for simplification include:

- Simplify DB schema: A severly-limited subset of field types is provided.
  There are no foreign key relations or field options. Field names correspond to
  familiar Python types. All fields have default values. Migrations are handled
  automatically. Within these constraints, django's full ORM is available.

- Simplify filesystem layout: Only two files are required: `models.py` and
  `views.py`. 


- Simplify management commands: There is a single command, `banjo`, which
  effectively runs django's `makemigrations`, `migrate`, and `runserver` in sequence.
  `banjo --shell` enters the REPL with all user-defined models loaded.

- Simplify request/response lifecycle: View functions receive a dict of params and 
  must return a dict. View-URL binding is handled by decorators, as in flask, and all
  URLs are static (there are no placeholders and no params are passed to the
  view).  Http errors are provided as exceptions, which simplifies control flow. 
  Models have `from_dict` (class method) and `to_dict` (instance method) helpers.

## Usage

Banjo can be instsalled with `pip install django-banjo`.

To write a Banjo app, create a folder called `app`, define models in `models.py` and 
define views in `views.py`. Here's a simple example. 

First, we define our models. Banjo provides four field types:

- `BooleanField` (`True`, `False`)
- `IntegerField` (`1`, `-102`)
- `FloatField` (`0.045`, `11.5`)
- `StringField` (`"alligator"`, `"hazelnut"`)

### `app/models.py`

    from banjo.models import Model, StringField

    class Animal(Model):
        name = StringField()
        sound = StringField()

Next we define our views. Each view is a function which receives a dict (called
`params` in the example below) and which must return a dict. Use the 
`banjo.urls.route_get` and `banjo.urls.route_post` decorators to route URLs to
your view functions. 
    
### `app/views.py`

    from banjo.urls import route_get, route_post
    from models import Animal
    
    @route('newanimal')
    def add_animal(params):
        animal = Animal.from_dict(params)
        animal.save()
        return animal.to_dict()

    @route('listen')
    def list_animal_sounds(params):
        sounds = []
        for animal in Animal.objects.all():
            sounds.append('{} says {}'.format(a.name, a.sound))     
        return {'sounds': sounds}

Now you can run `banjo` from the directory containing these files and the server
will start. Use the `--port` command to serve from a custom port; the default is
5000.

Here is an example of interacting with this app using the `httpie` command-line
utility:

    $ http localhost:5000/newanimal name=elehpant sound=pffffftttttt

    { 
      "name": "elephant",
      "sound": "pffffftttttt"
    }

    $ http localhost:5000/newanimal name=squirrel sound=chcheee

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


### HTTP errors

If something goes wrong and it's the client's fault, you can raise an error.
For example:

    from banjo.http import NotAllowed

    @route_get('error')
    def error(params):
        raise NotAllowed("I said no.")

The following errors are available in `banjo.http`:

- `BadRequest` (400)
- `Forbidden` (403)
- `NotFound` (404)
- `NotAllowed` (405)
- `ImATeapot` (418)

### Shell

You can also interact with your app's models from a Python shell. Just pass the
`--shell` argument to banjo:

    $ banjo --shell
    > Animal.objects.count()
    2

