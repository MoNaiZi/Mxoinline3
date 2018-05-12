from django.db import models
from datetime import datetime
#上面官方包 下面第三方（讲究)
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    #自定义性别选择规则
    GENDR_CHOICES=(
        ('male','男'),
        ('female','女')
    )
    #昵称（verbsoe_name就是取数据库导出成csv成的表的头一个字段）
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    #生日
    birthday = models.DateTimeField(verbose_name='生日',null=True,blank=True)
    #性别 只能男或女 ，默认女
    gender = models.CharField(
        max_length=5,
        verbose_name='性别',
        choices=GENDR_CHOICES,
        default='female'
    )
    #地址
    address = models.CharField(max_length=100,verbose_name='地址',default="")
    #电话
    mobile = models.CharField(max_length=11,null=True,blank=True)
    #头像 默认使用
    image = models.ImageField(
        upload_to='image/%Y/%M',
        default='image/default.png',
        max_length=100
    )

    #meta 信息，即后台栏目名
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

     #重载str方法，打印实例会打印username,username为继承自Abstractuser
     # ((待确认）直白点就是人性化显示对象属性）
    def __str__(self):
        return self.username


#邮箱验证码model
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register','注册'),
        ('forget','找回密码'),
    )

    code = models.CharField(max_length=20,verbose_name='验证码')
    #未设置null = true blank = true 默认不可为空
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(choices=SEND_CHOICES,max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    image = models.ImageField(
        upload_to='banner/%Y/%m',
        verbose_name='轮播图',
        max_length=100,
    )
    url = models.URLField(max_length=200,verbose_name='访问地址')
    #默认index很大靠后。想要靠前修改index值。
    index = models.IntegerField(default=100,verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

        4-6