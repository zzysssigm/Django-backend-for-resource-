# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import login
from django.contrib import messages
from .models import User, BlockList, Article, Post, Course, Reply, Notification
from .forms import ArticleForm, PostForm, ReplyForm
import random
import string
import re
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.generic.edit import CreateView

# 生成四位验证码,仅包含大小写字母和数字
def generate_email_code(length=4):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#发送验证码
def send_verification_email(email, code):
    subject = 'Your verification code'
    message = f'Your verification code is {code}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['passwd']
        email = request.POST['email']
        email_code = request.POST['email_code']
        
        # 校验验证码是否正确
        stored_email_code = request.session.get('register_email_code')
        if not stored_email_code:
            messages.error(request, '验证码已过期，请重新发送')
        elif email_code != stored_email_code:
            messages.error(request, '验证码错误')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, '用户名已存在')
            elif User.objects.filter(email=email).exists():
                messages.error(request, '电子邮件已注册')
            else:
                user = User(username=username, password=make_password(password), email=email)
                user.save()
                messages.success(request, '注册成功，请登录')
                return redirect('login_passwd')

    # 发送验证码
    if request.method == 'GET' and 'send_code' in request.GET:
        email = request.GET.get('email')
        if email:
            email_code = generate_email_code()
            request.session['register_email_code'] = email_code
            send_verification_email(email, email_code)
            messages.success(request, '验证码已发送，请检查您的邮箱')
    
    return render(request, 'register.html')

# 密码登录
def login_passwd(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        passwd = request.POST['passwd']

        try:
            user = User.objects.get(username=username)
            if check_password(passwd, user.password):
                login(request, user)
                messages.success(request, '登录成功')
                return redirect('homepage')
            else:
                messages.error(request, '密码错误')
        except User.DoesNotExist:
            messages.error(request, '用户不存在')
    return render(request, 'login_passwd.html')

# 邮箱验证码登录
def login_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_code = request.POST['email_code']

        # 校验验证码是否正确
        stored_email_code = request.session.get('login_email_code')
        if not stored_email_code:
            messages.error(request, '验证码已过期，请重新发送')
        elif email_code != stored_email_code:
            messages.error(request, '验证码错误')
        else:
            # 清除验证码
            del request.session['login_email_code']

            # 查找用户
            try:
                user = User.objects.get(email=email)
                # 用户存在，可以登录
                login(request, user)
                messages.success(request, '登录成功')
                return redirect('homepage')  # 登录成功后的重定向
            except User.DoesNotExist:
                messages.error(request, '用户不存在')

    # 发送验证码
    if request.method == 'GET' and 'send_code' in request.GET:
        email = request.GET.get('email')
        if email:
            email_code = generate_email_code()
            request.session['login_email_code'] = email_code
            send_verification_email(email, email_code)
            messages.success(request, '验证码已发送，请检查您的邮箱')
    
    return render(request, 'login_email.html')

@login_required
def homepage(request):
    blocklist = BlockList.objects.all()
    user = request.user
    articles = user.articles.all()
    notifications = Notification.objects.filter(user=user, read=False)
    # 调试打印
    # for article in articles:
    #     print(f"Article ID: {article.id}, Title: {article.article_title}")
    # print(user.id)
    return render(request, 'homepage.html', {'user': user,"block_list": blocklist, 'articles':articles, 'notifications': notifications })

@login_required
def delete_account(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email == request.user.email:
            email_code = generate_email_code()
            request.session['delete_account_email_code'] = email_code
            send_verification_email(email, email_code)
            messages.success(request, '验证码已发送到您的邮箱，请检查您的邮箱')
            return redirect('confirm_delete_account')
        else:
            messages.error(request, '邮箱地址不正确')

    return render(request, 'delete_account.html')

@login_required
def confirm_delete_account(request):
    if request.method == 'POST':
        email_code = request.POST['email_code']
        stored_email_code = request.session.get('delete_account_email_code')
        if not stored_email_code:
            messages.error(request, '验证码已过期，请重新发送')
            return redirect('delete_account_request')
        elif email_code != stored_email_code:
            messages.error(request, '验证码错误')
        else:
            user = request.user
            auth_logout(request)
            user.delete()
            messages.success(request, '您的账号已成功注销')
            return redirect('index')

    return render(request, 'confirm_delete_account.html')
# 重置密码
def reset_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        try:
            user = User.objects.get(username=username, email=email)
            email_code = generate_email_code()
            request.session['reset_email_code'] = email_code
            request.session['reset_user_id'] = user.id
            send_verification_email(email, email_code)
            messages.success(request, '验证码已发送，请检查您的邮箱')
            return redirect('reset_password_confirm')
        except User.DoesNotExist:
            messages.error(request, '用户名和电子邮件不匹配')

    return render(request, 'reset_password.html')

# 获得验证码后,输入用户名,验证码和新密码即可成功修改
def reset_password_confirm(request):
    if request.method == 'POST':
        username = request.POST['username']
        email_code = request.POST['email_code']
        new_password = request.POST['new_password']

        stored_email_code = request.session.get('reset_email_code')
        user_id = request.session.get('reset_user_id')

        if not stored_email_code or not user_id:
            messages.error(request, '验证码已过期，请重新发送')
        elif email_code != stored_email_code:
            messages.error(request, '验证码错误')
        else:
            try:
                user = User.objects.get(id=user_id, username=username)
                user.password = make_password(new_password)
                user.save()
                del request.session['reset_email_code']
                del request.session['reset_user_id']
                messages.success(request, '密码重置成功，请登录')
                return redirect('login_passwd')
            except User.DoesNotExist:
                messages.error(request, '用户不存在')

    return render(request, 'reset_password_confirm.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

def index(request):
    return render(request,'index.html')

def userlist(request):
    datalist=User.objects.all()
    blocklist = BlockList.objects.all()
    articles = Article.objects.all()
    return render(request,"userlist.html",{"data_list":datalist,"block_list": blocklist,"articles":articles})

@login_required
def block_user(request):
    if request.method == 'POST':
        current_user_id = request.POST.get('current_user_id')
        block_user_id = request.POST.get('block_user_id')
        
        try:
            current_user = User.objects.get(pk=current_user_id)
            user_to_block = User.objects.get(pk=block_user_id)
            
            if current_user == user_to_block:
                messages.error(request, "不能拉黑自己")
                return redirect('homepage')
            
            # 检查是否已经拉黑
            if BlockList.objects.filter(from_user=current_user, to_user=user_to_block).exists():
                messages.error(request, "用户已经在黑名单中")
            else:
                # 添加到黑名单
                BlockList.objects.create(from_user=current_user, to_user=user_to_block)
                messages.success(request, "用户已成功拉黑")
        
        except User.DoesNotExist:
            messages.error(request, "用户不存在")
        
    # return redirect('userlist')
    # return redirect('homepage')
    # 重定向到带参数的页面需要传参args
    return redirect(reverse('user_homepage', args=[block_user_id]))

@login_required
def unblock_user(request, user_id):
    user_me = request.user
    user_to_unblock = get_object_or_404(User, id=user_id)

    # 检查是否存在拉黑关系
    block_entry = BlockList.objects.filter(from_user=user_me, to_user=user_to_unblock).first()
    if block_entry:
        block_entry.delete()
        message = "已成功解除黑名单！"
    else:
        message = "你还没有拉黑此用户！"

    return render(request, 'unblock_result.html', {'message': message})

@login_required
def blocklist(request):
    user_me = request.user
    blocked_users = user_me.blocking.all()
    # for blu in blocked_users:
    #     print(blu.from_user)
    #     print(blu.to_user)
    return render(request, 'block_list.html', {'blocked_users': blocked_users})


@login_required
def user_homepage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_me = request.user
    articles = user.articles.all()
    return render(request, 'otherpage.html', {'user': user, 'user_me':user_me, 'articles': articles})

# 好像没啥用，直接搞个按钮传回去得了
# @login_required
# def return_homepage(request):
#     return redirect('homepage')

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, '文章发表成功')
            return redirect('user_homepage', user_id=request.user.id)
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})


# @login_required
# def article_detail(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     user_me = request.user
#     user = article.author
#     # 检查是否被作者拉黑
#     if BlockList.objects.filter(from_user=user, to_user=user_me).exists():
#         return render(request, 'user_be_blocked.html',{'user':user})
#     # print(article.id)
#     # print(article.article_title)
#     return render(request, 'article_detail.html', {'article': article})

@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    user_me = request.user
    user = article.author

    # 检查是否被作者拉黑
    if BlockList.objects.filter(from_user=user, to_user=user_me).exists():
        return render(request, 'user_be_blocked.html', {'user': user})

    # 获取文章相关的帖子及其回复
    posts = Post.objects.filter(article=article).prefetch_related('replies')

    context = {
        'article': article,
        'posts': posts,
    }

    return render(request, 'article_detail.html', context)

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)
    if request.method == 'POST':
        article.delete()
        messages.success(request, '文章删除成功')
        return redirect('user_homepage', user_id=request.user.id)
    
    return render(request, 'confirm_delete.html', {'article': article})

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, '文章修改成功')
            return redirect('user_homepage', user_id=request.user.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'edit_article.html', {'form': form, 'article': article})

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    # api:形如http://127.0.0.1:8000/media/images/C9STJRL5WPZTXLHY9V.jpg
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'image': serializer.data['image']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'  

    def form_valid(self, form):
        article_id = self.kwargs['article_id']
        # print(article_id)
        article = get_object_or_404(Article, id=article_id)
        form.instance.article = article
        form.instance.poster = self.request.user
        post = form.save()
        mentioned_user=article.author
        post.send_notification(mentioned_user)
        return super().form_valid(form)

    def get_success_url(self):
        article_id = self.kwargs['article_id']
        # print(article_id)
        return reverse('article_detail', kwargs={'article_id': article_id})

class PostCreateCourse(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'  

    def form_valid(self, form):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        form.instance.course = course
        form.instance.poster = self.request.user
        post = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        course_id = self.kwargs['course_id']
        return reverse('course_detail', kwargs={'course_id': course_id})

class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_form.html'

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        form.instance.post = post
        form.instance.replier = self.request.user
        reply = form.save()
        mentioned_user = post.poster
        reply.send_notification(mentioned_user)
        #  这个不需要检查[@]
        #  self.check_and_notify(reply)

        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        if post.course:  # 检查 post 是否关联到 Course
            return reverse('course_detail', kwargs={'course_id': post.course.id})
        else:
            return reverse('article_detail', kwargs={'article_id': post.article.id})

    # def check_and_notify(self, reply):
    #     pattern = r'^\[@(\w+)\]'
    #     match = re.match(pattern, reply.reply_content)
    #     if match:
    #         username = match.group(1)
    #         try:
    #             mentioned_user = User.objects.get(username=username)
    #             reply.send_notification(mentioned_user)
    #         except User.DoesNotExist:
    #             pass

class ReplyToReplyView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_form.html'

    def form_valid(self, form):
        parent_reply_id = self.kwargs['reply_id']
        parent_reply = get_object_or_404(Reply, id=parent_reply_id)
        post = parent_reply.post
        form.instance.post = post
        form.instance.replier = self.request.user
        form.instance.reply_content = f"[@{parent_reply.replier.username}] {form.cleaned_data['reply_content']}"
        reply = form.save()

        # 检查是否有提到的用户并发送通知
        self.check_and_notify(reply)

        return super().form_valid(form)

    def get_success_url(self):
        parent_reply_id = self.kwargs['reply_id']
        parent_reply = get_object_or_404(Reply, id=parent_reply_id)
        post = parent_reply.post
        if post.course:  # 检查 post 是否关联到 Course
            return reverse('course_detail', kwargs={'course_id': post.course.id})
        else:
            return reverse('article_detail', kwargs={'article_id': post.article.id})

    def check_and_notify(self, reply):
        pattern = r'^\[@(\w+)\]'
        match = re.match(pattern, reply.reply_content)
        if match:
            username = match.group(1)
            try:
                mentioned_user = User.objects.get(username=username)
                reply.send_notification(mentioned_user)
            except User.DoesNotExist:
                pass

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('homepage')

@login_required
def course_list(request):
    courses=Course.objects.all()
    return render(request, 'course_list.html',{'courses':courses})

@login_required
def course_detail(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    # 获取课程相关的帖子及其回复
    posts = Post.objects.filter(course=course).prefetch_related('replies')
    context = {
        'course': course,
        'posts': posts,
    }
    return render(request, 'course_detail.html', context)