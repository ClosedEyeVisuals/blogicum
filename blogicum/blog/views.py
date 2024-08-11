from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone as tz
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, PostForm, UserUpdateForm
from .mixins import CommentEditMixin, OnlyAuthorMixin, PostEditMixin
from .models import Category, Comment, Post
from .utils import get_posts_queryset

MAX_POSTS_PER_PAGE = 10

User = get_user_model()


class HomePage(ListView):
    model = Post
    queryset = get_posts_queryset()
    template_name = 'blog/index.html'
    paginate_by = MAX_POSTS_PER_PAGE


class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = MAX_POSTS_PER_PAGE

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        author = self.object
        object_list = get_posts_queryset(
            manager=author.posts,
            is_filtered=self.request.user != author
        )
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
            kwargs={'username': self.object.username}
        )


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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

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
        context['comments'] = self.object.comments.select_related(
            'author')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.author.username}
        )


class PostUpdateView(PostEditMixin, OnlyAuthorMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostDeleteView(PostEditMixin, OnlyAuthorMixin, DeleteView):
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(CommentEditMixin, OnlyAuthorMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentEditMixin, OnlyAuthorMixin, DeleteView):
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class UserCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')
