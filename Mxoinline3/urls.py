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
from users.views import LoginView,LogoutView,RegisterView,ForgetPwdView,ActiveUserView,ResetView,ModifyPwdView
from django.conf.urls import url,include
from django.views.static import serve
from Mxoinline3.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # TemplateView.as_view会将template转换为view
    url('^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url('^login/$',LoginView.as_view(),name='login'),
    url('^users/',include('users.urls',namespace='users')),
    url('^logout/$',LogoutView.as_view(),name='logout'),
    url('^register/$',RegisterView.as_view(),name='register'),
    url('^captcha/',include('captcha.urls')),
    url('^forget/$',ForgetPwdView.as_view(),name= 'forget_pwd'),
    url('^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name = 'user_active'),
    url('^reset/(?P<active_code>.*)/$',ResetView.as_view(),name='reset_pwd'),
    url('^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),
    url('^org/', include('organization.urls',namespace='org')),
    # 处理图片显示的url,使用django自带serve，传入参数告诉它去那个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^course/',include('courses.urls',namespace='course'))
]



