# encoding: utf-8
__author__ = 'ZMY'
__date__ = '2018/5/14 0009 21:05'

import xadmin
from .models import UserAsk,UserCourse,UserMessage,UserFavorite,CourseComments


# 用户咨询后台管理器
class UserAskAdmin(object):
    list_display = ['name','mobile','course_name','add_time']
    search_fields = ['name','mobile','course_name']
    list_filter = ['name','mobile','course_name','add_time']
    model_icon = "fa fa-address-card-o"


# 用户课程学习后台管理器
class UserCourseAdmin(object):
    list_display = ['user','course','add_time']
    search_fields = ['user','course']
    list_filter = ['user','course','add_time']
    model_icon = "fa fa-address-card-o"


# 用户消息后台管理器
class UserMessageAdmin(object):
    list_display = ['user','message','has_read','add_time']
    search_fields = ['user','message','has_read']
    list_filter = ['user','message','has_read','add_time']
    model_icon = "fa fa-bell-o"


# 用户评论后台管理器
class CourseCommentsAdmin(object):
    list_display = ['user','course','comments','add_time']
    search_fields = ['user','course','comments']
    list_filter = ['user','course','comments','add_time']
    model_icon = "fa fa-comment-o"


# 用户收藏后台管理器
class UserFavoriteAdmin(object):
    list_display = ['user','fav_id','fav_type','add_time']
    search_fields = ['user','fav_id','fav_type']
    list_filter = ['user','fav_id','fav_type','add_time']
    model_icon = 'fa fa-star-o'


# 将后台管理与models进行关联
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)