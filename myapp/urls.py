from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ImageViewSet, ImageUploadView

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
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('create_article/', views.create_article, name='create_article'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('confirm_delete_account/', views.confirm_delete_account, name='confirm_delete_account'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('block_user/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('blocklist', views.blocklist, name='block_list'),
    path('upload_image/', ImageUploadView.as_view(), name='upload_image'),
    path('', include(router.urls)),
]
