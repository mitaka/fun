from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from registration.forms import RegistrationForm
from captcha.fields import CaptchaField
from core.models import Author, Post

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['receive_update']

class PostForm(forms.ModelForm):
    content = forms.CharField(label=_('Content'), widget=SummernoteInplaceWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'keywords']

class CaptchaRegistrationForm(RegistrationForm):
    captcha = CaptchaField()
