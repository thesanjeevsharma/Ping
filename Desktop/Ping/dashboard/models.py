from django.contrib.auth.models import Permission, User
from django.db import models
from django import forms

# Create your models here.
class Post(models.Model):
    post_pic = models.ImageField()
    post_text = models.TextField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)
    post_by = models.ForeignKey(User, default=1)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return (str(self.post_by) + ' - ' + str(self.post_text))

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(max_length=140)
    comment_by = models.ForeignKey(User, related_name='comments')

    def __str__(self):
        return (str(self.comment_by) + ' - ' + str(self.comment_text))

    def total(self):
        return self.Comment.all().count()
