from django.db import models
from datetime import datetime

#引入网民CourseComments所需要的外键models
from users.models import UserProfile
from courses.models import Course


#用户我要学习表单
class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name='姓名')
    mobile = models.CharField(max_length=11,verbose_name='手机')
    course_name = models.CharField(max_length=50,verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


#用户对于课程评论
class UserFavorite(models.Model):
    #会涉及四个外键。用户，课程，机构，讲师import
    TYPE_CHOICES = (
        (1,'课程'),
        (2,'课程机构'),
        (3,'讲师'),
    )
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    # course = models.ForeignKey(Course,verbose_name='课程')
    # teacher = models.ForeignKey()
    # org = models.ForeignKey()
    # fav_type =

    #机智版
    #直接保存用户的Id
    fav_id = models.IntegerField(default=0)
    #表明收藏的是那种类型.
    fav_type= models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='收藏数'
    )
    add_time = models.DateTimeField(default=datetime.now,verbose_name='评论时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


#用户消息表
class UserMessage(models.Model):
    #因为我们的消息有两种：发给全员和发给某一个用户。
    #所以如果使用外键，每个消息会对应要有用户，很难实现全员消息

    #机制版 为0发给所有用户，不为0就是发给用户的id
    user = models.IntegerField(default=0,verbose_name='接收用户')
    message = models.CharField(max_length=500,verbose_name='消息内容')

    #是否已读：布尔类型 BooleanField False未读，True表示已读
    has_read = models.BooleanField(default=False,verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='用户消息'
        verbose_name_plural = verbose_name


#用户课程表



