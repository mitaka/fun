from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.translation import ugettext_lazy as _
from core.models import Post, Author, Tag, Category, Rating, NewsLetter

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
    queryset.update(sent=True)
send_newsletters.short_description = _("Send selected Newsletters")

class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sent', 'date_updated', 'date_created', 'date_sent']
    filter_display = ['sent']
    actions = ['send_newsletters']
admin.site.register(NewsLetter, NewsLetterAdmin)
