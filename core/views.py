from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from core.models import Post, Author, Category, Rating
from core.forms import AuthorForm, PostForm
from core.utils import get_query
from core.mixins import PostOwnerMixin


class PostListView(ListView):
    queryset = Post.objects.select_related()
    paginate_by = 20


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = get_object_or_404(Author, username=self.request.user.username)
        return super(PostCreateView, self).form_valid(form)


class PostEditView(PostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm


class CategoryCreateView(CreateView):
    model = Category
    success_url = '/'


class CategoryListPostsView(ListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['name'])
        return Post.objects.filter(category=self.category)


class AuthorDetailView(DetailView):
    model = Author

    def get_object(self, queryset=None):
        return self.request.user


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required()
def rating_up(request, id=None, slug=None):
    if id is not None and slug is not None:
        post_obj = get_object_or_404(Post, pk=id)
        try:
            Rating(post=post_obj, user=request.user, rating=1).save()
            messages.success(request, _('Vote registered'))
            cache_key = make_template_fragment_key('object_list')
            cache.delete(cache_key)
        except IntegrityError:
            messages.warning(request, _('You already voted for this.'))
        except:
            messages.error(request, _('Unable to register your vote.'))
    return HttpResponseRedirect(reverse('post', kwargs={"pk": id, "slug": slug}))


@login_required()
def rating_down(request, id=None, slug=None):
    if id is not None and slug is not None:
        post_obj = get_object_or_404(Post, pk=id)
        try:
            Rating(post=post_obj, user=request.user, rating=-1).save()
            messages.success(request, _('Vote registered'))
            cache_key = make_template_fragment_key('object_list')
            cache.delete(cache_key)
        except IntegrityError:
            messages.warning(request, _('You already voted for this.'))
        except:
            messages.error(request, _('Unable to register your vote.'))
    return HttpResponseRedirect(reverse('post', kwargs={"pk": id, "slug": slug}))


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'content', ])
        found_entries = Post.objects.filter(entry_query).order_by('-last_update')
    return render_to_response('core/search_results.html', {'query_string': query_string, 'found_entries': found_entries}, context_instance=RequestContext(request))
