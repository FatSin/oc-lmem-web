import os
from django.apps import AppConfig


class SearchappConfig(AppConfig):
    if os.environ.get('ENV') == 'PRODUCTION':
        #name = 'lememeenmieux.searchapp'
        name = 'lememeenmieux.cestapps.searchapp'
    else:
        name = 'searchapp'


