from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from registration.forms import RegistrationForm
from captcha.fields import CaptchaField
from core.models import Author, Post, NewsLetter
from core.widgets import AdminImageWidget, SummernoteCustomWidget

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['email', 'username', 'first_name', 'last_name', 'receive_update', 'jabber_contact', 'avatar']
        widgets = {
            'avatar': AdminImageWidget
        }

class PostForm(forms.ModelForm):
    content = forms.CharField(label=_('Content'), widget=SummernoteInplaceWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'keywords', 'unsafe']

class NewsLetterForm(forms.ModelForm):
    content = forms.CharField(label=_('Content'), widget=SummernoteCustomWidget())

    class Media:
        model = NewsLetter

class CaptchaRegistrationForm(RegistrationForm):
    captcha = CaptchaField()
