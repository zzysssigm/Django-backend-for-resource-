# 测试用文档

使用Django自带的templates进行了前端功能的简单测试，以下页面和功能均已测试完成：

`index.html`:测试使用的主页，集成了各个页面的跳转，方便测试，对应url为/user/index/；

`userlist.html`：打印了所有用户的信息，包括id，用户名，密码，邮箱，拉黑关系等，对应url为/user/userlist/；

`register.html`：为用户提供注册功能，需要输入用户名，密码，邮箱以及邮件验证码，对应url为/user/register/，目前使用个人邮箱发送验证码；

`login_email.html`：为用户提供邮箱登录功能，需要输入用户名，邮箱以及邮件验证码，对应url为/user/login_email/，完成验证后验证码将会过期，以保证安全；

`login_passwd.html`：为用户提供密码登录功能，需要输入用户名和密码，对应url为/user/login_passwd/；

使用Django自带的会话功能（sessions），会话周期为两周，在这段时间里用户无需多次登录；在用户主页提供了登出功能，可以直接结束会话；

`homepage.html`：用户的个人主页，需要登陆后(@login_required)才能访问，对应url为/user/homepage/；在用户主页可以看到用户的所有文章，除非被作者block；

`otherpage.html`：其他用户的主页，需要登陆后才能访问，对应url为/user/homepage/<user.id>/；

`reset_password.html`：提供了重置密码功能，用户需要输入用户名和邮箱进行校验，校验成功则向用户邮箱发送验证码，并进入confirm环节；

`reset_password_confirm.html`：输入用户名，密码和邮箱验证码，通过校验后可以进行重置，对应url为/user/reset_password_confirm/；

`delete_account.html`：提供了注销账户功能，用户需要输入用户名和邮箱进行校验，校验成功则向用户邮箱发送验证码，并进入confirm环节

`confirm_delete_account.html`：输入邮箱验证码并确认，通过校验后可以进行重置，对应url为/user/delete_password_confirm/；

`create_article.html`：用户可以创作并发表文章，目前还是纯文本，对应url为/user/create_article/；

`article_detail.html`：用户可以通过自己或者他人的用户界面查看文章内容，对应url为/user/article/<article.id>/；

图片api调用：正常进行文章编辑时，点击`插入图片`，即可将图片上传到服务器，并在光标处生成对应url，形如/media/images/example.jpg；

`confirm_delete.html`：确认是否删除文章，对应url为/article/delete/<article.id>/；

`edit_article.html`：提供修改文章的功能，对应url为/article/edit/<article.id>/；

`block_list.html`：查看用户黑名单，可以对黑名单中的用户进行解封操作（unblock），对应url为/user/blocklist；

## 已完成的功能：

（1）基础用户功能：实现了 账密登陆/邮箱登陆/注册/重置密码/退出登陆/注销账户 等功能；

（2）进阶用户功能：实现了 个人主页/黑名单/拉黑/解除拉黑 等功能，可以访问他人主页；可以 发布/删除/修改 文章；

主页可以看到用户发布的所有文章，被拉黑则不能；

文章使用markdown渲染，插入图片会自动在光标处生成url；

（3）课程功能：开发中

## 接下来的任务：

明天做post和course；然后展示文章时候检测是否block（这个其实交给前端就可以，展示的时候检查一下是否block）；

设置管理员权限；

主页再多装饰一点东西，比如用户的posts，以及通知；

验证码发送需要时间间隔（比如60s），待完善逻辑；

地理位置检测功能还未上线，不过应该简单；

tags可以考虑使用#分隔，就不用单独存每个tag了；

图片api调用时的鉴权，没想好怎么做；

最麻烦的通知功能/回复功能/发帖功能，慢慢琢磨吧，感觉好复杂啊，目前是打算：发replytoreply和post都会带一个[@{username}]，但post中的@不会渲染出来，reply中的会；

比较重要的course类，把这个写好就基本成型了；

### 1.User类

储存用户信息的类。

`class User(AbstractUser)`继承自AbstractUser类，其对象定义如下：

```python
# AbstractUser类自带的id,username和password;其中id是自增类型
# 验证码,由随机生成的四位字符组成，仅包含大小写字母和数字
email_code = models.IntegerField(null=True, blank=True)
# 信誉值，过低会处以封禁
reputation = models.IntegerField(default=100)
# 收获的总点赞
all_likes = models.IntegerField(default=0)
# 文章收获的总浏览量
all_views = models.IntegerField(default=0)
# 影响力指数
influence = models.IntegerField(default=0)
# 是否是管理员
master = models.BooleanField(default=False)
# 是否被封禁
block = models.BooleanField(default=False)
# 封禁结束时间
block_end_time = models.DateTimeField(null=True, blank=True)
# 用户的黑名单
blocklist = models.ManyToManyField('self', symmetrical=False, 
                                   related_name='blocked_by', through='BlockList')
# 用户的发出的所有post

# 用户的收到的所有reply（@信息和post下的评论都简化成reply）
```

### 2.Block_list类

储存用户之间拉黑操作的类。

`class BlockList(models.Model)`定义如下：

```python
    # block的发起者
    from_user = models.ForeignKey(User, related_name='blocking', on_delete=models.CASCADE)
    # 被block的用户
    to_user = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
    # 操作执行时间
    created_at = models.DateTimeField(auto_now_add=True)
    #表示一对一的约束关系
    class Meta:
        unique_together = ('from_user', 'to_user')
```

### 3.Article类

储存文章的类。

`class Article(models.Model)`定义如下：

```python
    # 文章的id
    id = models.AutoField(primary_key=True)
    # 文章标题
    article_title = models.CharField(max_length=255)
    # 作者（与User类关联）
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    # 文章内容
    content = models.TextField()
    # 标签
    tags = models.CharField(max_length=255)
    # 点赞数量（或者收藏数量？）
    stars = models.IntegerField(default=0)
    # 浏览数量
    views = models.IntegerField(default=0)
    # 该文章是否被屏蔽
    block = models.BooleanField(default=False)
    # 应该再加一个：保护期，如果被屏蔽就不能被其他用户看到，但不会直接删除，直到保护期后再删除

    # 发表时间
    publish_time = models.DateTimeField(auto_now_add=True)
    # 图片url等，存起来然后记录插入位置？暂时还没想好怎么处理

    def __str__(self):
        return self.article_title
```

### 4. Post类


### 5. reply类


### 6. course类


### 

### 其他指令备忘录：

#### （1）Django的迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

#### (2)项目启动：

```shell
python manage.py runserver
```

#### (3)启动mysql服务

```shell
sudo service mysql start
```

#### (4)登陆到mysql

```shell
mysql -u root -p[passwd]
```
注意没有空格

#### (5)临时开启代理

```shell
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```
git修改代理配置：

```shell
git config --global --get http.proxy
git config --global --get https.proxy
```

#### mysqlclient安装失败

见https://www.cnblogs.com/xingxia4/p/17832964.html；

#### 设置自增id从某个数值开始（如1000000）

可以迁移完成后手动在mysql中修改。

```mysql
ALTER TABLE myapp_user AUTO_INCREMENT = 1000000;
```