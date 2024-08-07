from django import forms
from .models import Article, Post, Reply

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['article_title', 'content', 'tags']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'content', 'tags', 'block', 'top']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_content']
