import os
import sys
from django.apps import AppConfig

sys.path.append(sys.path[0] + "/../lememeenmieux")

class SearchappConfig(AppConfig):
    if os.environ.get('ENV') == 'PRODUCTION':
        name = 'lememeenmieux.searchapp'
    else:
        name = 'searchapp'


