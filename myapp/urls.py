from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ImageViewSet, ImageUploadView, PostCreateView, ReplyCreateView, ReplyToReplyView, PostCreateCourse

router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login_passwd/', views.login_passwd, name='login_passwd'),
    path('login_email/', views.login_email, name='login_email'),
    path('logout/', views.logout, name='logout'),
    path('userlist/', views.userlist, name='userlist'),
    path('homepage/', views.homepage, name='homepage'),
    path('homepage/<int:user_id>/', views.user_homepage, name='user_homepage'),
    path('notifications/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articlelist/', views.articlelist, name='articlelist'),
    path('create_article/', views.create_article, name='create_article'),
    path('article/delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('article/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('article/<int:article_id>/post/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/reply/', ReplyCreateView.as_view(), name='create_reply'),
    path('reply/<int:reply_id>/reply/', ReplyToReplyView.as_view(), name='reply_to_reply'),
    path('reply/delete/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('confirm_delete_account/', views.confirm_delete_account, name='confirm_delete_account'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('block_user/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('blocklist', views.blocklist, name='block_list'),
    path('courselist/', views.course_list, name='courselist'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('create_course/', views.create_course, name='create_course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('course/<int:course_id>/post/', PostCreateCourse.as_view(), name='create_post_course'),
    path('upload_image/', ImageUploadView.as_view(), name='upload_image'),
    path('like/<int:content_type_id>/<int:object_id>/', views.like_item, name='like_item'),
    path('', include(router.urls)),
]
