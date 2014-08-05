from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.template.defaultfilters import slugify
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from unidecode import unidecode
from django.contrib.sitemaps import ping_google
from core.utils import send_html_mail
import hmac
import hashlib

class AuthorUserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            msg = _('Users must have valid email address')
            raise ValueError(msg)

        if password is None:
            msg = _('Please supply password')
            raise ValueError(msg)

        if username is None:
            msg = _('Please supply username')

        now = timezone.now()
        user = self.model(email=AuthorUserManager.normalize_email(email),
                        username=username,
                        is_staff=False, is_active=False, is_superuser=False,
                        last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        secret = bytes(user.email, 'utf-8')
        data = bytes(user.username, 'utf-8')
        digest = hmac.new(secret, data, digestmod=hashlib.sha256)
        user.registration_hash = digest.hexdigest()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Author(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'),unique=True)
    username = models.CharField(_('Username'), max_length=50, unique=True)
    first_name = models.CharField(_('First Name'), max_length=150)
    last_name = models.CharField(_('Last Name'), max_length=150)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    receive_update = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'),default=timezone.now)
    registration_hash = models.CharField(max_length=64, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AuthorUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_short_name(self):
        return "%s" % self.first_name

    def get_fullast_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_username(self):
        return "%s" % self.email

    def get_absolute_url(self):
        return "/author/%s/" % urlquote(self.pk)

    def email_user(self, subject, message, from_email=None):
        a = self.username
        send_mail(subject, message, from_email, [self.email])

    def activate_user(self, user, hash):
        if self.username == user:
            secret = bytes(self.email).encode('utf-8')
            data = bytes(self.username).encode('utf-8')
            computed_hash = hmac.new(secret, data, digestmod=hashlib.sha256).hexdigest()
            if self.registration_hash == hash and self.registration_hash == computed_hash:
                self.is_active = True
                self.save()
                return True
            else:
                return False

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=50, db_index=True)

    def __unicode__(self):
        return "%s" % self.name    

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return "%s" % self.name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    category = models.ForeignKey(Category)
    author = models.ForeignKey(Author)
    date_created = models.DateTimeField(default=timezone.now, db_index=True)
    last_update = models.DateTimeField(default=timezone.now)
    tag = models.ManyToManyField(Tag, related_name="tag_name")
    keywords = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255,blank=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(unidecode(self.title[:255]))
        super(Post, self).save(*args,**kwargs)
        try:
            ping_google(sitemap_url='/sitemap.xml')
        except Exception():
            pass
        context = {"title": self.title, "url": "http://fun.mitaka-g.net/post/" + str(self.pk) + "/" + self.slug + "/"}
        with open ("/home/django/projects/fun/core/templates/core/post_email.txt", "r") as myfile:
            t = myfile.read().replace('\n', '')
        template = Template(t)
        for author in Author.objects.filter(receive_update=True):
            if author.pk == self.author.pk:
                continue
            send_html_mail('New post on fun.mitaka-g.net', template.render(Context(context)), 'webmaster@fun.mitaka-g.net', [author.email], fail_silently=False)

    def __unicode__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        return "/post/" + str(self.id) + "/" + self.slug + "/"

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Author)
    post = models.ForeignKey(Post)
    rating = models.IntegerField()

    class Meta:
        unique_together = (('user','post'))

    def get_rating(self, post):
        return Rating.objects.filter(post__pk=post).aggregate(Avg('rating'))
