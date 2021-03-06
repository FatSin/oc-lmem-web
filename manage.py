#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    #if os.environ.get('ENV') == 'PRODUCTION':
    sys.path.append(sys.path[0] + "/../lememeenmieux")
    sys.path.append(sys.path[0] + "/../lememeenmieux/lememeenmieux")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lememeenmieux.lememeenmieux.settings")

    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lememeenmieux.settings")
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lememeenmieux.lememeenmieux.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
