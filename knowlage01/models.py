from django.db import models

class user(models.Model):
    uid=models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=64,verbose_name='用户名',unique=True)
    password=models.IntegerField(verbose_name='密码')
    nickname=models.CharField(max_length=64,unique=True,verbose_name='昵称')
    email=models.EmailField(null=True,verbose_name='邮箱')
    avator=models.ImageField(verbose_name='头像',upload_to='static/img')
    create_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class fans(models.Model):
    faned=models.ForeignKey(to='user',to_field='uid',related_name='faned')
    fan=models.ForeignKey(to='user',to_field='uid',related_name='fan')
    class Meta:
        unique_together=[
            ('faned','fan'),
        ]
    def __str__(self):
        return "%s-%s"%(self.faned.username,self.fan.username)
class blog(models.Model):
    bid=models.BigAutoField(primary_key=True)
    title=models.CharField(verbose_name='博客标题',max_length=64)
    theme=models.CharField(verbose_name='博客主题',max_length=64)
    site=models.CharField(verbose_name='博客后缀',max_length=64,unique=True)
    user=models.OneToOneField(to='user',to_field='uid')
    def __str__(self):
        return self.title

class content(models.Model):
    id = models.BigAutoField(primary_key=True)
    content=models.TextField(verbose_name='文章内容')
    article=models.OneToOneField(verbose_name='所属文章',to='article',to_field='aid',null=True)
    def __str__(self):
        return self.article.title
class classfiy(models.Model):
    id = models.BigAutoField(primary_key=True)
    classfiy=models.CharField(verbose_name='分类',max_length=64)
    blog=models.ForeignKey(verbose_name='所属博客',to='blog',to_field='bid')

    def __str__(self):
        return "%s-%s"%(self.blog.title,self.classfiy)

class tag(models.Model):
    tid = models.BigAutoField(primary_key=True)
    tag=models.CharField(verbose_name='标签',max_length=64)
    blog=models.ForeignKey(verbose_name='所属博客',to='blog',to_field='bid')
    def __str__(self):
        return "%s-%s"%(self.blog.title,self.tag)
class article(models.Model):
    aid=models.BigAutoField(primary_key=True)

    title=models.CharField(verbose_name='文章题目',max_length=64)
    summary=models.CharField(verbose_name='文章摘要',max_length=225)
    create_time=models.DateTimeField(verbose_name='发布时间',auto_now_add=True)
    read_count=models.IntegerField(verbose_name='阅读数')
    comment_count=models.IntegerField(verbose_name='评论数')
    up_count=models.IntegerField(verbose_name='点赞数',null=True)
    dowm_count=models.IntegerField(verbose_name='点踩数',null=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='blog', to_field='bid')
    classfiy=models.ForeignKey(verbose_name='分类',to='classfiy',to_field='id',null=True)
    type_choice=[
        (1,'Python'),
        (2,'Linux'),
        (3,'Go'),
        (4,'Java')
    ]
    type=models.IntegerField(verbose_name='类型',choices=type_choice,default=None)

    def __str__(self):
        return "%s-%s"%(self.blog.title,self.title)

class article_tag(models.Model):
    article=models.ForeignKey(to='article',to_field='aid',null=True)
    tag=models.ForeignKey(to='tag',to_field='tid',null=True)
    class Meta:
        unique_together=[
            ('article','tag')
        ]
    def __str__(self):
        return "%s-%s"%(self.article.title,self.tag.tag)
class updown(models.Model):
    user=models.ForeignKey(verbose_name='点赞/踩的用户',to='user',to_field='uid')
    article=models.ForeignKey(verbose_name='点赞的文章',to='article',to_field='aid')
    type=models.BooleanField(verbose_name='是否赞')
    class Meta:
        unique_together=[
            ('user','article')
        ]
    def __str__(self):
        return self.article.title

class comment(models.Model):
    id=models.BigAutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='评论的用户', to='user', to_field='uid')
    article = models.ForeignKey(verbose_name='评论的文章', to='article', to_field='aid')
    create_time=models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
    content=models.CharField(verbose_name='评论内容',max_length=225)
    parent_id=models.ForeignKey(verbose_name='回复评论',to='self',null=True)

    def __str__(self):
        return "%s-%s-%s"%(self.article.title,self.user.username,self.content)