from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
# from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
# from example.config import pagination
from django.db.models import Q # for search option


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# def pagination(request, data, num=10):
#     paginator = Paginator(data, num)
#     page = request.GET.get('page')

#     try:
#         items = paginator.page(page)
#     except PageNotAnInteger:
#         items = paginator.page(1)
#     except EmptyPage:
#         items = paginator.page(paginator.num_pages)

#     index = items.number - 1
#     max_index = len(paginator.page_range)
#     start_index = index - 5 if index >= 5 else 0
#     end_index = index + 5 if index <= max_index -5 else max_index
#     page_range = paginator.page_range[start_index:end_index]

#     return items, page_range

# for search option
def search(request):
    template = 'blog/home.html'
    query = request.GET.get('q')
    results = Post.objects.filter(Q(title__icontains = query) | Q(content__icontains = query))
    # pages = pagination(request, results, num=1)
    context = {
        'posts': results,
        # 'items': pages[0],
        # 'page_range': pages[1],
    }
    return render(request, template, context)
