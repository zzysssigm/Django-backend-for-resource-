# 测试用文档

## 已完成的功能：

（1）基础用户功能：实现了 账密登陆/邮箱登陆/注册/重置密码/退出登陆/注销账户 等功能，地理位置检测还未上线；用户id还需完善（比如从10000000开始）；

（2）进阶用户功能：实现了 个人主页/黑名单/拉黑/解除拉黑 等功能，可以访问他人主页；主页可以看到用户发布的所有文章，被拉黑则不能；

（3）

## 接下来的任务：

主页再多装饰一点东西，比如用户的posts；

文章的图片显示功能，需要建个端口专门存图片，然后渲染时根据url渲染，注意检测过大的图片，不太了解这方面；

最麻烦的通知功能/回复功能/发帖功能，慢慢琢磨吧，感觉好复杂啊

然后是最重要的course类，明天写吧，把这个写好基本成型了就

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

# 用户的所有article

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
    article_id = models.AutoField(primary_key=True)
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
    # 图片url等，没想好怎么处理

    def __str__(self):
        return self.article_title
```

### 4. Post类


### 5. reply类


### 6. course类


### 

### 其他指令：

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