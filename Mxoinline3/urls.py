"""Mxoinline3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView,LogoutView,RegisterView,ForgetPwdView,ActiveUserView,ResetView,ModifyPwdView,IndexView
from django.conf.urls import url,include
from django.views.static import serve
from Mxoinline3.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 富文本编辑器
    url('ueditor/',include('DjangoUeditor.urls')),
    # TemplateView.as_view会将template转换为view
    url('^$',IndexView.as_view(),name='index'),
    url('^login/$',LoginView.as_view(),name='login'),
    # 用户个人中心
    url('^users/',include('users.urls',namespace='users')),
    # 登出
    url('^logout/$',LogoutView.as_view(),name='logout'),
    # 注册
    url('^register/$',RegisterView.as_view(),name='register'),
    url('^captcha/',include('captcha.urls')),
    url('^forget/$',ForgetPwdView.as_view(),name= 'forget_pwd'),
    url('^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name = 'user_active'),
    url('^reset/(?P<active_code>.*)/$',ResetView.as_view(),name='reset_pwd'),
    url('^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),
    # 课程机构
    url('^org/', include('organization.urls',namespace='org')),
    # 处理图片显示的url,使用django自带serve，传入参数告诉它去那个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 静态文件
    # url(r'^static/(?P<path>.*)$',serve,{'document_root':STATIC_ROOT}),
    # 公开课
    url(r'^course/',include('courses.urls',namespace='course'))
]

# 全局404页面配置
handler404 = 'users.views.pag_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'

