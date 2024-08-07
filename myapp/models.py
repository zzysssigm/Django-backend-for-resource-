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


class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('compulsory', 'Compulsory'),        # 必修课
        ('elective', 'Elective'),            # 选修课
        ('restricted_elective', 'Restricted Elective'),  # 限选课
    ]

    COURSE_METHOD_CHOICES = [
        ('online', 'Online'), # 线上
        ('offline', 'Offline'), # 线下
        ('hybrid', 'Hybrid'), # 混合
    ]

    id = models.AutoField(primary_key=True)  # 自增id, 自动设为主键
    course_name = models.CharField(max_length=255) # 课程名
    course_type = models.CharField(max_length=50, choices=COURSE_TYPE_CHOICES) # 课程类型
    college = models.CharField(max_length=255) # 开设大学
    credits = models.DecimalField(max_digits=4, decimal_places=2) # 学分
    course_teacher = models.CharField(max_length=255) # 课程老师
    course_method = models.CharField(max_length=50, choices=COURSE_METHOD_CHOICES) # 教学方式
    assessment_method = models.CharField(max_length=255) # 考核方式
    likes = models.PositiveIntegerField(default=0) # 点赞数
    # score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00) 怎么感觉没啥用
    relative_articles = models.ManyToManyField(Article, related_name='courses')
    publish_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=255)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    tags = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    block = models.BooleanField(default=False)
    top = models.BooleanField(default=False)
    publish_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)

    def send_notification(self, mentioned_user):
        Notification.objects.create(
            user=mentioned_user,
            message=f"Your article have a new post, title:{self.post_title[:50]}, content:{self.content[:50]}"  # 通知消息可以包含帖子内容的前50个字符
        )

    def __str__(self):
        return self.post_title

class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    reply_content = models.TextField()
    reply_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    replier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    
    def send_notification(self, mentioned_user):
        Notification.objects.create(
            user=mentioned_user,
            message=f"You were mentioned in a reply: {self.reply_content[:50]}"  # 通知消息可以包含回复内容的前50个字符
        )

    def __str__(self):
        return f'Reply to {self.post.post_title} by {self.replier.username}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"

    class Meta:
        ordering = ['-created_at']

class Test(models.Model):
    age=models.IntegerField(default=2)