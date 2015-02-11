from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.translation import ugettext_lazy as _

from core.models import Post, Author, Tag, Category, Rating, NewsLetter
from core.utils import read_template
from core.forms import NewsLetterForm

class InlineRating(admin.TabularInline):
    model = Rating
    extra = 0

class PostAdmin(SummernoteModelAdmin):
    inlines = (InlineRating,)
admin.site.register(Post, PostAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['email', '__str__', 'username', 'is_active']
    filter_display = ['is_active']
admin.site.register(Author, AuthorAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

def send_newsletters(modeladmin, request, queryset):
    for letter in queryset:
        context = {
            'subject': letter.subject,
            'content': letter.content,
        }
        template = read_template("/home/django/projects/fun/core/templates/core/post_newsletter_email.txt")
        for author in Author.objects.filter(newsletter=True):
            send_gearman_mail(letter.subject, template.render(Context(context)), 'webmaster@fun.mitaka-g.net', [author.email], fail_silently=False, auth_user=settings.MANDRILL_USER, auth_password=settings.MANDRILL_API_KEY, host=settings.MANDRILL_HOST)
            queryset.update(sent=True)
send_newsletters.short_description = _("Send selected Newsletters")

class NewsLetterAdmin(admin.ModelAdmin):
    form = NewsLetterForm
    list_display = ['subject', 'sent', 'date_updated', 'date_created', 'date_sent']
    filter_display = ['sent']
    actions = ['send_newsletters']
admin.site.register(NewsLetter, NewsLetterAdmin)
