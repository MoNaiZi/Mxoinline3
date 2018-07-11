# encoding: utf-8
__author__ = 'ZMY'
__date__ = '2018/6/28 8:46'

from .views import UserInfoView,UserMyCourse,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView
from .views import MyFavOrgView,MyFavTeacherView,FavCourse,MyMessageView
from django.conf.urls import url

app_name = 'users'

urlpatterns = [
    # 用户信息
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),
    # 用户头像
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload'),
    # 用户密码修改
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name='update_pwd'),
    # 邮箱验证码
    url(r'^sendemail_code/$',SendEmailCodeView.as_view(),name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(),name='update_email'),
    # 用户课程
    url(r'^mycourse/$',UserMyCourse.as_view(),name='user_mycourse'),
    # 用户收藏课程机构
    url(r'^fav_org/$',MyFavOrgView.as_view(),name='fav_org'),
    # 用户收藏讲师
    url(r'^fav_teacher/$',MyFavTeacherView.as_view(),name='fav_teacher'),
    # 用户收藏公共课
    url(r'^fav_course/$',FavCourse.as_view(),name='fav_course'),
    # 用户消息
    url(r'^message/$',MyMessageView.as_view(),name='message')

]