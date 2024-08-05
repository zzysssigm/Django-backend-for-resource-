from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser

# 继承AbstractUser,自带id,username和password
class User(AbstractUser):
    email_code = models.IntegerField(null=True, blank=True)
    reputation = models.IntegerField(default=100)
    all_likes = models.IntegerField(default=0)
    all_views = models.IntegerField(default=0)
    influence = models.IntegerField(default=0)
    master = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    block_end_time = models.DateTimeField(null=True, blank=True)
    blocklist = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by', through='BlockList')

    def __str__(self):
        return self.username

class BlockList(models.Model):
    from_user = models.ForeignKey(User, related_name='blocking', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    content = models.TextField()
    tags = models.CharField(max_length=255)
    stars = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    block = models.BooleanField(default=False)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article_title

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s image {self.id}"

class Test(models.Model):
    age=models.IntegerField(default=2)