from django.urls import include, path

from . import views

app_name = 'blog'

post_urls = [
    path(
        'create/',
        views.PostCreateView.as_view(),
        name='create_post',
    ),
    path(
        '<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path(
        '<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        '<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        '<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('posts/', include(post_urls)),
    path(
        'category/<slug:slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts',
    ),
    path(
        'profile/edit_profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile',
    ),
    path(
        'profile/<username>/',
        views.ProfileDetailView.as_view(),
        name='profile',
    ),
    path(
        'auth/registration/',
        views.UserCreateView.as_view(),
        name='registration',
    ),
]
