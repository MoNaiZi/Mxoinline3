# encoding: utf-8
from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher


# 课程信息
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj','初级'),
        ('zj','中级'),
        ('gj','高级'),
    )
    course_org = models.ForeignKey(CourseOrg,verbose_name='所属机构',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name='课程名')
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',null=True,blank=True)
    you_need_know = models.CharField(max_length=300,default='一颗勤学的心是本课程必要前提',verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300,default='要乖乖乖哦0.0',verbose_name='老师告诉你')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    tag = models.CharField(max_length=15,verbose_name='课程标签',default='')
    category = models.CharField(max_length=20,default="后端开发",verbose_name='课程类别')
    # TextField可以输入无限大
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField('是否轮播',default=False)
    degree = models.CharField(choices=DEGREE_CHOICES,max_length=2)
    # 使用分钟做后台记录（存储最小单位）前台转换
    learn_times = models.IntegerField(default=0,verbose_name='学习时长（分钟数)')
    # 保存学习人数：点击开始学习才算
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(
        upload_to='courses/%Y/%m',
        verbose_name='封面图',
        max_length=100,
    )
    # 保存点击量,点击页面就算
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    def get_zj_nums(self):
        # 获取课程章节数的方法 lesson_ste 反向取值
        return self.lesson_set.all().count()


    # 获取学习这门课程的用户
    def get_learn_users(self):
        # 谁的里面添加了Course（自己）做外键，它都可以取出来(现在是反向取）
        return self.usercourse_set.all()

    # 获取课程章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name


#章节
class Lesson(models.Model):
    # 因为一个课程对应很多章节。所以在章节表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个章节对应哪个课程
    course = models.ForeignKey(Course,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    # 获取章节视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return '<<{0}>>课程的章节 >> {1}'.format(self.course,self.name)

    class Meta:
        verbose_name='章节'
        verbose_name_plural = verbose_name


#每章视频
class Video(models.Model):
    # 因为一个章节对应很多视频。所以在视频表中将章节设置为外键
    # 作为一个字段来存储让我们可以知道这个视频对应哪个章节。
    lesson = models.ForeignKey(Lesson,verbose_name='章节')
    name = models.CharField(max_length=100,verbose_name='视频名')
    url = models.CharField(max_length=200,default='http://zhongminyong.tech',verbose_name='访问地址')
    learn_times = models.IntegerField(default=0,verbose_name='学习时长（分钟数)')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    image = models.FileField(
        default='',
        upload_to= "teacher/%Y/%m",
        verbose_name='视频',
        max_length= 255,
        null= True,
        blank= True,
    )

    def __str__(self):
        return '{0}章节的视频 >> {1}'.format(self.lesson,self.name)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural=verbose_name


# 课程资源
class CourseResource(models.Model):
    # 因为一个课程对应很多资源，所以在课程资源表中将课程设置为外键
    # 作为一个字段来让我们知道这个资源对应哪个课程
    course = models.ForeignKey(Course,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='名称')
    # 这里定义成文件类型field,后台管理系统中会直接有上传的按钮。
    # FileField也是一个字符串类型，要指定最大长度。
    download = models.FileField(
        upload_to='course/%Y/%m',
        verbose_name='资源文件',
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='课程资源'
        verbose_name_plural=verbose_name
