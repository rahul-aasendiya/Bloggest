from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','author','category','content')


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment',)