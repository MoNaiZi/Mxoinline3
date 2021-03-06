from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View
from courses.models import Course,CourseResource
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from operation.models import UserFavorite,CourseComments,UserCourse
from .models import Video
from users.models import Banner
from django.http import HttpResponse
# django 自带的用法，要求登陆
from django.contrib.auth.mixins import LoginRequiredMixin


class CourseListView(View):
    """
    公开课列表
    """
    def get(self,request):
        all_course = Course.objects.all()

        # 进行排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students': # 对应html sort=hot
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')

        # 热门课程推荐
        hot_courses = Course.objects.all().order_by("-students")[:3]
        # 搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q 可以实现多个字段，之间是or关系
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        # 对课程进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_course中取出来，每页显示2个
        p = Paginator(all_course,2,request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_course':courses,
            'sort':sort,
            'hot_courses':hot_courses,
            'search_keywords':search_keywords,
        })


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self,request,course_id):
        # 此处的id为表，默认为我们添加的值
        course = Course.objects.get(id = int(course_id))
        # 增加课程点击数
        course.click_nums +=1
        course.save()

        # 是否收藏课程
        has_fav_course = False
        # 收藏机构
        has_fav_org = False
        # 必须是用户已登录我们才需要判断(没有登陆就给个匿名用户，登陆就执行下面的语句）
        if not request.user.is_authenticated :
            # *
            if UserFavorite.objects.filter(user = request.user,fav_id = course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user = request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            # 从1开始否则会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org':has_fav_org,
        })


# 处理课程章节信息页面
class CourseInfoView(LoginRequiredMixin,View):
    # 要求登陆才能进
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self,request,course_id):

        # 此处的id为表默认为什么添加的值
        course = Course.objects.get(id = int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        course.students +=1
        course.save()
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course = course)
        # 从关系中取出user_id
        user_ids = [user_courses.user_id for user_courses in user_courses]
        # 这些用户学了的课程，外键会自动有id取到字段
        all__user_courses = UserCourse.objects.filter(user_id__in = user_ids)
        # 取出所有课程id
        course_ids = [all__user_courses.course_id for all__user_courses in all__user_courses]
        # 获取学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click_nums')[:5]
        # 是否收藏课程

        return render(request,'course-video.html',{
            'course':course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
        })
    # 重点：两个下划线代表我传进来的是一个list，你进行遍历


# 配置课程评论的url和view
class CommentsView(View):
    def get(self,request,course_id):
        # 此处的id为表默认为我们添加的值
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.all()
        return render(request,'course-comment.html',{
            'course':course,
            'all_resources':all_resources,
            'all_comment':all_comment,
        })


# ajax方式添加评论
class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # get只能取出一条数据，如果有多条抛出异常。没有数据也不会抛异常
            course = Course.objects.get(id = int(course_id))
            # 外键存入要存入对象
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}',content_type='application/json')


# 播放视频的view
class VideoPlayView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        # 找到对应的course
        course = video.lesson.course
        # 查询用户是否开始学习了该课，如果未学习则，加入用户课程表
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        # 查询课程资源
        all_resources = CourseResource.objects.filter(course=course)
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        user_ids = [user_course.user_id for user_course in user_courses ]
        # 这些用户学了的课程，外键会自动有id ，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过其他的课程
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click_nums').exclude(id=course.id)[:4]
        # 是否收藏课程
        return render(request,'course-play.html',{
            'course':course,
            'all_resources':all_resources,
            'relate_courses': relate_courses,
            'video':video,
        })