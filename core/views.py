from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib import messages

from core.models import Post, Author, Category, Rating
from core.forms import AuthorForm, PostForm

class PostListView(ListView):
    model = Post
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    fields = ['title', 'content', 'category', 'keywords']

    def form_valid(self, form):
        form.instance.author = get_object_or_404(Author, username=self.request.user.username)
        return super(PostCreateView, self).form_valid(form)

class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    fields = ['title', 'content', 'category', 'keywords']

class CategoryCreateView(CreateView):
    model = Category
    success_url = '/'

class AuthorDetailView(DetailView):
    model = Author

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['email', 'username', 'first_name', 'last_name', 'receive_update']

@login_required()
def rating_up(id=None):
    if id is not None:
        post_obj = get_object_or_404(Post, pk=id)
        try:
            Rating(post=post_obj, user=request.user, rating=1).save()
            messages.success(request,_('Vote registered'))
        except:
            messages.error(request,_('Unable to register your vote'))
    return HttpResponseRedirect(reverse('post',kwargs={"pk": id, "slug": slug}))

@login_required()
def rating_down(id=None):
    if id is not None and slug is not None:
        post_obj = get_object_or_404(Post, pk=id)
        try:
            Rating(post=post_obj, user=request.user, rating=-1).save()
            messages.success(request,_('Vote registered'))
        except:
            messages.error(request,_('Unable to register your vote'))
    return HttpResponseRedirect(reverse('post',kwargs={"pk": id, "slug": slug}))
