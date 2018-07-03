from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View
from .models import CourseOrg,CityDict,Teacher
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from organization.forms import AnotherUserForm
from operation.models import UserFavorite
from courses.models import Course
# 课程机构列表的view
class OrgView(View):
    def get(self,request):
        # 查找到所有的课程机构
        all_orgs = CourseOrg.objects.all()
        # 取出所有城市
        all_citys = CityDict.objects.all()
        # 授课机构，如果不加负号会是由小到大
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 取出筛选的城市，默认值为空
        city_id = request.GET.get('city','')
        # 如果选择了某个城市，也就是前端传过来的值
        if city_id:
            # 外键city在数据中叫city_id
            # 我们就在机构中作进一步筛选
            all_orgs  = all_orgs.filter(city_id = int(city_id))

        # 类别筛选
        category = request.GET.get('ct','')
        if category:
            # 我们就在机构中作进一步筛选类别
            all_orgs = all_orgs.filter(category = category)

         # 总共有多少家机构使用count进行统计
        org_nums = all_orgs.count()

        # 进行排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 机构搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__contains=search_keywords))

        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取5个出来，每页显示5个
        p = Paginator(all_orgs,5,request = request)
        orgs = p.page(page)

        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
        })


# 用户添加我要学习
class AddUserAskView(View):
    # 处理表单提交当然post
    def post(self,request):
        userask_form = AnotherUserForm(request.POST)
        # 判断该form是否有效
        if userask_form.is_valid():
            # 这里是modelform和form的区别
            # 它有model的属性
            # 当commit为true 进行真正保存
            user_ask = userask_form.save(commit = True)
            # 这样就不需要把一个一个字段取出来然后存到model的对象中之后在save

            # 如果保存成功，返回json字符串，后面content type是告诉浏览器的,
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            # 如果保存失败，返回json字符串，并将form的报错信息通过msg传到前端
            return HttpResponse("{'status':'fail','msg':{0}}".format(userask_form.errors), content_type = 'application/json')



class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = 'home' # 向org_base传递值，表明现在在home页
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()[:4] #
        all_teacher = course_org.teacher_set.all()[:2] #

        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page': current_page
        })



class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current_page = 'course'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id)) #
        # 通过课程机构找到课程，内建变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()

        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page

        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self,request,org_id):
        # 向前端传值，表明现在在desc页
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到了指定这个字段的外键引用
        # 向前端传值说明用户是否收藏
        has_fav = False
        # 必须是用户已登录我们才需要判断
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user = request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgTeacherView(View):
    """
    机构讲师列表页
    """
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_teachers = course_org.teacher_set.all() # teacher_set 就是讲师Teachers
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })
        # has_fav = False
        # 必须是用户已登录我们才需要判断
        # if request.user.is_authenticated:
        #     if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
        #         has_fav = True
        #     return render(request,'org-detail-teachers.html',{
        #         'all_teachers':all_teachers,
        #         'course_org':course_org,
        #         'current_page':current_page,
        #         'has_fav':has_fav
        #     })



class AddFavView(View):
    """
    用户收藏与取消收藏功能
    """
    def post(self,request):
        # 表明你收藏的不管是课程，还是机构，他们的id
        # 默认值取0是因为空串转int报错
        id = request.POST.get('fav_id',0)
        # 取到你收藏的类别，从前台提交的ajax请求中取
        type = request.POST.get('fav_type',0)

        # 收藏与已收藏取消收藏
        # 判断用户是否登录:即使没登陆会有一个匿名的user
        if not request.user.is_authenticated():
            # 未登录是返回json提示未登录,跳转到登录页面实在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(id),fav_type=int(type))
        if exist_records:
            # 如果已经存在，则 表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}',content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 过滤掉未取到fav_id type默认情况
            if int(type) >0 and int(id) >0:
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


            # 向前端传值说明用户是否收藏
            # has_fav = False
            # # 必须是用户已登录我们才需要判断
            # if request.user.is_authenticated:
            #     if UserFavorite.objects.filter(user = request.user,fav_id = course_org.id,fav_type=2):
            #         has_fav = True
            # return render(request, 'org-detail-homepage.html', {
            #     'all_courses': all_courses,
            #     'all_teacher': all_teacher,
            #     'course_org': course_org,
            #     "current_page": current_page,
            #     "has_fav": has_fav
            # })


# 授课教师列表页
class TeacherListView(View):
    def get(self,request):
        all_teacher = Teacher.objects.all()
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teacher.count()
        # 排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teacher = all_teacher.order_by('-click_nums')

        # 排行榜讲师
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]

        # 搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))
        # 对讲师进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取出五个出来，每页显示1个
        p = Paginator(all_teacher,2,request=request)
        teachers = p.page(page)
        return render(request,'teachers-list.html',{
            'all_teacher':teachers,
            'teacher_nums':teacher_nums,
            'sort':sort,
            'rank_teacher':rank_teacher
        })


# 讲师详情页面
class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        all_course = teacher.course_set.all()
        # 排行榜讲师
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]
        # 收藏
        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
            has_fav_org = True
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'rank_teacher': rank_teacher,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })