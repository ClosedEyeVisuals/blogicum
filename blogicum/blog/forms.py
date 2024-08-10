from django.forms import DateInput, ModelForm

from .models import Comment, Post, User


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'category',
            'location',
            'is_published',
            'image',
        )
        widgets = {
            'pub_date': DateInput(attrs={'type': 'date'})
        }


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
