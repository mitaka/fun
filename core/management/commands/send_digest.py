from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.conf import settings
from django.db.models import Q
from datetime import datetime, timedelta
from core.models import Author, Post
from core.utils import send_gearman_mail, read_template

class Command(BaseCommand):
    help = 'Sends daily digest mails to anyone subscribed'

    def handle(self, *args, **kwargs):
        days_diff = 1
        post_list = {}
        post_list['posts'] = list()

        for post in Post.objects.filter(date_created__gte=datetime.now()-timedelta(days=days_diff)):
            context = {}
            context['title'] = post.title
            context['url'] = "http://fun.mitaka-g.net/post/" + str(post.pk) + "/" + post.slug + "/"
            post_list['posts'].append(context)

        if post_list['posts'].len == 0:
            return

        template = read_template('/home/django/projects/fun/core/templates/core/post_digest_email.txt')

        for author in Author.objects.filter(Q(receive_update=2) & Q(is_active=True)):
            send_gearman_mail('Daily digest for fun.mitaka-g.net', template.render(Context(post_list)), 'webmaster@fun.mitaka-g.net', [author.email], fail_silently=False, auth_user=settings.MANDRILL_USER, auth_password=settings.MANDRILL_API_KEY, host=settings.MANDRILL_HOST)
            
