HTTP errors
===========

If something goes wrong and it’s the client’s fault, you can raise an
error. For example, you might add another view to ``app/views.py``:

::

   from banjo.http import Forbidden

   @route_get('secrets')
   def do_not_show_the_secrets(params):
       raise Forbidden("Nice try.")

Again, from the command line:

::

   $ http GET localhost:8000/secrets
   HTTP/1.1 403 Forbidden

   {
       "error": "Nice try."
   }

The following errors are available in ``banjo.http``:

-  ``BadRequest`` (400)
-  ``Forbidden`` (403)
-  ``NotFound`` (404)
-  ``NotAllowed`` (405)
-  ``ImATeapot`` (418)

