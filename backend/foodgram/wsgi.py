import os, sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ilya/dev/foodgram-project-react/backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodgram.settings")
application = get_wsgi_application()