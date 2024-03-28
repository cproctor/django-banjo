Models
======

Banjo's Model class extends Django's with ``from_dict`` and ``to_dict`` methods, 
which are important for Banjo's use case: consuming JSON requests and 
producing JSON responses.

Banjo's ModelField classes wrap Django's, adding default values and 
required cascade behavior for foreign keys. 

.. automodule:: banjo.models
   :members:
   :undoc-members:
   



