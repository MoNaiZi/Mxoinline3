# encoding: utf-8
__author__ = 'mtianyan'
__date__ = '2018/6/14 21:01'

from courses.views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView,VideoPlayView
from django.conf.urls import url

app_name = 'courses'

urlpatterns = [
    # 公开课列表
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    # 课程详情页
    url('^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    # 章节信息
    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),
    # 课程评论
    url(r'^comments/(?P<course_id>\d+)/$',CommentsView.as_view(),name='course_comments'),
    # 添加评论
    url(r'all_comment/',AddCommentsView.as_view(),name='add_comment'),
    # 课程视频播放页
    url(r'^video/(?P<video_id>\d+)/$',VideoPlayView.as_view(),name='video_play'),
]