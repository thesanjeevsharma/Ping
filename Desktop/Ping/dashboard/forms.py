from django import forms

from .models import Post, Comment, User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_pic', 'post_text']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text']