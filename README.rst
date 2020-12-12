==========
Payanpaadu
==========

Payanpaadu is a re-usable Django app that can be plugged into other Django application across Tandora code bases where Django is used.

Detailed documentation is in the `wiki <https://bitbucket.org/tandoraco/payanpaadu/wiki/Home>`_.

Available modules
_________________

1. Email backend
    - Mailgun
2. Storage
    - Azure

Installation
------------

Quick start
-----------

1. Add "payanpaadu" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'payanpaadu',
    ]

