from django.forms import ModelForm

from .models import Comment, User


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
