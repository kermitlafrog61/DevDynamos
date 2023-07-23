from celery import Celery

from .settings import settings


app = Celery('core')
app.config_from_object(settings)
app.conf.imports = ('apps.auth.tasks', )
