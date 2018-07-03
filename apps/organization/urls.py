# encoding: utf-8
__author__ = 'mtianyan'
__date__ = '2018/5/31 8:03'

from organization.views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,TeacherListView
from organization.views import OrgDescView,OrgTeacherView,AddFavView,TeacherDetailView
from django.conf.urls import url

app_name = 'organization'

urlpatterns = [
    # 课程机构
    url('^list/',OrgView.as_view(),name='org_list'),
    # 添加我要学习
    url('^add_ask/',AddUserAskView.as_view(),name='add_ask'),
    # home页面,取纯数字
    url(r'home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    # 访问机构课程
    url('^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    # 访问机构描述
    url('^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(), name='org_desc'),
    # 访问机构讲师
    url('^teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),
    # 机构收藏
    url('^add_fav/',AddFavView.as_view(),name='add_fav'),
    # 讲师列表
    url(r'teacher_list/',TeacherListView.as_view(),name='teacher_list'),
    # 讲师详情
    url(r'^teacher/detail/(?P<teacher_id>\d+)/',TeacherDetailView.as_view(),name='teacher_detail')

]