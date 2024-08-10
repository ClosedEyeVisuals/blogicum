from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CommentEditMixin:
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_object(self):
        return get_object_or_404(
            Comment,
            post_id=self.kwargs['post_id'],
            pk=self.kwargs['comment_id'],
        )


class PostEditMixin:
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
