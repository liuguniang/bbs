from django.db import models

class User(models.Model):
   username=models.CharField(verbose_name='用户名',max_length=32)
   password=models.CharField(verbose_name='密码',max_length=64)
   email=models.EmailField(verbose_name='邮箱')

   def __str__(self):
       return self.username

class Role(models.Model):
    caption=models.CharField(verbose_name='角色',max_length=32)
    def __str__(self):
        return self.caption
class User2Role(models.Model):
    user=models.ForeignKey(User,verbose_name='用户',related_name='roles')
    role=models.ForeignKey(Role,verbose_name='角色',related_name='users')
    def __str__(self):
        return '%s-%s'%(self.user.username,self.role.caption)

class Menu(models.Model):
    caption=models.CharField(verbose_name='菜单名称',max_length=32)
    parent=models.ForeignKey('self',verbose_name='父菜单',related_name='p',null=True,blank=True)
    def __str__(self):
        prev = ""
        parent = self.parent
        while True:
            if parent:
                prev = prev + '-' + str(parent.caption)
                parent = parent.parent
            else:
                break
        return '%s-%s' % (prev, self.caption,)

class Permission(models.Model):
    caption=models.CharField(verbose_name='权限',max_length=32)
    url=models.CharField(verbose_name='url正则',max_length=128)
    menu=models.ForeignKey(Menu,verbose_name='所属菜单',related_name='permission',null=True,blank=True)

    def __str__(self):
        return '%s-%s'%(self.caption,self.url)
class Action(models.Model):
    caption=models.CharField(verbose_name='操作',max_length=32)
    code=models.CharField(verbose_name='方法',max_length=32)
    def __str__(self):
        return self.caption
class Permission2Role2Action(models.Model):
    permission=models.ForeignKey(Permission,verbose_name='权限url',related_name='actions')
    action=models.ForeignKey(Action,verbose_name='操作',related_name='permissions')
    role=models.ForeignKey(Role,verbose_name='角色',related_name='p2as')
    class Meta:
        unique_together=(
            ('permission','action','role'),
        )
    def __str__(self):
        return '%s-%s-%s'%(self.permission,self.action,self.role)
