import os
from django.apps import AppConfig


class SearchappConfig(AppConfig):
    if os.environ.get('ENV') == 'PRODUCTION':
        name = 'lememeenmieux.searchapp'
    else:
        name = 'searchapp'

        
