from django.conf import settings
from django.template import Context
from core.utils import read_template, send_gearman_mail

import logging
logger = logging.getLogger(__name__)


def post_save_user(sender, instance, created, **kwargs):
    context = {"user": instance.username, "email": instance.email}

    if created:
        template = read_template('core/templates/registration/registration_email.txt')
        send_gearman_mail('User registration', template.render(Context(context)), 'webmaster@fun.mitaka-g.net', [settings.ADMIN_EMAIL], fail_silently=False, auth_user=settings.MANDRILL_USER, auth_password=settings.MANDRILL_API_KEY, host=settings.MANDRILL_HOST)
