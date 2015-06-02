import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fun.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if os.environ['DEBUG']:
    import uwsgi
    from uwsgidecorators import timer
    from django.utils import autoreload

    @timer(3)
    def change_code_gracefull_reload(sig):
	    if autoreload.code_changed():
		    uwsgi.reload()
