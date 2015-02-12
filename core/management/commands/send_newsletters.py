from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.utils import timezone
from django.conf import settings
from core.models import Author, NewsLetter
from core.utils import send_gearman_mail, read_template

class Command(BaseCommand):
    help = 'Sends newsletters'

    def handle(self, *args, **kwargs):
        for nl in NewsLetter.objects.filter(sent=False):
            context = {"subject": nl.subject, "content": nl.content}
            template = read_template('/home/django/projects/fun/core/templates/core/post_newsletter_email.txt')
            for author in Author.objects.all():
                send_gearman_mail(nl.subject, template.render(Context(context)), 'webmaster@fun.mitaka-g.net', [author.email], fail_silently=False, auth_user=settings.MANDRILL_USER, auth_password=settings.MANDRILL_API_KEY, host=settings.MANDRILL_HOST)
                nl.date_sent = timezone.now()
                nl.sent = True
                nl.save()
