from django.shortcuts import render
import json
from django.contrib.auth import authenticate,login,logout
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm,RegisterForm,ForgetForm,ActiveForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_eamil
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from courses.models import Course
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from .models import Banner
from django.shortcuts import render_to_response

# 自定义authenticate方法
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
# 并集运算
from django.db.models import Q


# 首页
class IndexView(View):
    def get(self,request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播图课程
        banner_courses = Course.objects.filter(is_banner=True)[:2]
        # 课程机构
        course_org = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_org':course_org,
        })


# 404
def pag_not_found(request):
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


# 505
def page_error(request):
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response


# sql注入测试代码（登陆）
# class LoginUnsafeView(View):
#     def get(self,request):
#         return render(request,'login.html',{})
#     def post(self,request):
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#
#         import MySQLdb
#         conn = MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = 'root',db = 'mxonline3', charset = 'utf8')
#         cursor = conn.cursor()
#         sql_select = "select * from users_userprofile where email='{0}' and  password='{1}'".format(user_name,pass_word)
#         result = cursor.execute(sql_select)
#         for row in cursor.fetchall():
#             # 查询到用户
#             pass
#         print('test')


class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict（查询集)所以直接传入
        # POST中的username password,会对应到form中
        login_form = LoginForm(request.POST)

        # is_valid 判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')

            user = authenticate(username = user_name,password = pass_word)

            if user is not None:
                login(request,user)
                return render(request,'index.html')
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误!'})

        else:
            return render(request,'login.html',{'login_form':login_form})


# 登出
class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 注册功能的view
class RegisterView(View):
    def get(self,request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email',"")
            pass_word = request.POST.get('password',"")

            #实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            #加密进行报存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送邮件
            send_register_eamil(user_name,'register')
            pass


# 激活用户的view
class ActiveUserView(View):
    def get(self,request,active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request)
        # 如果不为空也就是有用户
        for record in all_record:
            # 获取对应的邮箱
            email = record.email
            # 查找到邮箱对应的user
            user = UserProfile.objects.get(email = email)
            user.is_active  = True
            user.save()
            # 激活成功跳转到登陆页面
            return  render(request,'login.html',)
        # 验证码错误
        else:
            return render(request,'register.html',{'msg':'您的激活链接无效','active_form':active_form})



# 用户忘记密码的处理view
class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self,request):
        forget_from = ForgetForm()
        return render(request,'forgetpwd.html',{ })

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码邮件
            send_register_eamil(email, 'forget')
            # 发送完毕返回登录页面并显示发送邮件成功
            return render(request, 'login.html', {'msg': '重置密码邮件已发送，请注意查收'})
            # 如果表单验证失败也就是他验证码输错等
        else:
            return render(request,'forgetpwd.html',{'forget_from':forget_form})



# 重置密码的view
class ResetView(View):
    def get(self,request,active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将email传回来
                return render(request,'password_reset.html',{'email':email})
        # 验证码错误
        else:
            return render(
                request,'forgetpwd.html',{
                    'msg':'您的重置密码链接无效，请重新请求','active_form':active_form
                }
            )


# 改变密码的view
class ModifyPwdView(View):
    def post(self,request):
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
            pwd1 = request.POST.get('password1',"")
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')

            # 如果两次密码不想等，返回错误信息
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})

            # 密码一致
            user= UserProfile.objects.get(email = email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request,'login.html',{'msg':'密码修改成功，请登录'})
        # 验证失败说明密码位数不够
        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modiypwd_form':modiypwd_form})


# 实现用户名邮箱均可登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能一个。Q为使用并集查询
            user = UserProfile.objects.get(Q(username = username)|Q(email = username))

            # django的后台中密码加密：所以不能password == passowrd
            # UserProfile继承的AbstractUser中有def check_passoword(self,raw_password):

            if user.check_password(password):
                return user
                
        except Exception as e:
            return None


# 用户个人信息
class UserInfoView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        # 这是修改不是创建一个新的。需要指明instance.不然无法修改，而是新增用户
        user_info_form = UserInfoForm(request.POST,instance = request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



# 用户头像修改
class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        # 上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}',content_type='application/json')


# 用户密码修改
class UpdatePwdView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next',

    def post(self,request):
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type='application/json')
            # 如果密码一致
            user = request.user
            # 加密
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        # 验证失败说明密码位数不够
        else:
            return HttpResponse(json.dumps(modiypwd_form.errors),content_type='application/json')


# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        # 取出需要发送的邮件
        email = request.GET.get('email','')

        # 不能使已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}',content_type='application/json')
        send_register_eamil(email,'update_email')
        return HttpResponse('{"status":"success"}',content_type='application/json')


# 修改新邮箱+验证验证码
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}',content_type='application/json')


# 用户课程
class UserMyCourse(View):
    def get(self,request):
        all_course = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'all_course':all_course,
        })


# 用户收藏公共课
class FavCourse(View):
    def get(self,request):
        course = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_cours in fav_courses:
            course_id = fav_cours.fav_id
            cou = Course.objects.get(id=course_id)
            course.append(cou)
        return render(request,'usercenter-fav-course.html',{
            'course':course,
        })


# 用户收藏的课程机构
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id 也就是机构的id
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list
        })


# 用户收藏讲师
class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self,request):
        teacher_list = []
        fav_teacher = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for teacher in fav_teacher:
            teacher_id = teacher.fav_id
            tea = Teacher.objects.get(id=teacher_id)
            teacher_list.append(tea)
        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list,
        })


# 我的消息
class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message,4,request=request)
        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            'messages':messages
        })