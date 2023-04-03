from django.core.wsgi import get_wsgi_application

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")

application = get_wsgi_application()
