#!/usr/bin/env python
import os
import sys

useProductionDatabase=False

if __name__ == '__main__':
    if useProductionDatabase:
        try:
            import set_production_environment_variables
        except:
            raise Exception('You need a set_production_environment_variables.py file to access production database')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Package-Beast-API.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
