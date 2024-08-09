from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone as tz
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, UserUpdateForm
from .models import Category, Comment, Post

MAX_POSTS_PER_PAGE = 10

User = get_user_model()


def get_posts_queryset(manager=Post.objects):
    return manager.filter(
        pub_date__lt=tz.now(),
        is_published=True,
        category__is_published=True
    ).select_related(
        'author',
        'category',
        'location',
    )


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class HomePage(ListView):
    model = Post
    queryset = get_posts_queryset()
    template_name = 'blog/index.html'
    paginate_by = MAX_POSTS_PER_PAGE


class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    context_object_name = 'profile'
    paginate_by = MAX_POSTS_PER_PAGE

    def get_context_data(self, **kwargs):
        author = self.object
        if self.request.user == author:
            object_list = author.posts.select_related(
                'author',
                'category',
                'location',
            )
        else:
            object_list = get_posts_queryset(manager=author.posts)

        context = super(ProfileDetailView, self).get_context_data(
            object_list=object_list,
            **kwargs
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'slug': self.object.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return Post.objects.filter(
            Q(
                pub_date__lt=tz.now(),
                is_published=True,
                category__is_published=True
            ) | Q(author=self.request.user.id))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related(
            'author')
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'blog/category.html'
    queryset = Category.objects.filter(is_published=True)
    paginate_by = MAX_POSTS_PER_PAGE

    def get_context_data(self, **kwargs):
        object_list = get_posts_queryset(manager=self.object.posts)
        context = super(CategoryDetailView, self).get_context_data(
            object_list=object_list,
            **kwargs
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = (
        'title',
        'text',
        'pub_date',
        'category',
        'location',
        'image',
    )
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'slug': self.object.author.username}
        )


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    fields = (
        'title',
        'text',
        'pub_date',
        'category',
        'location',
        'image',
    )
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def handle_no_permission(self):
        return redirect('blog:post_detail', pk=self.kwargs['pk'])


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    current_post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.current_post
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'pkc'
    template_name = 'blog/comment.html'


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'pkc'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})
