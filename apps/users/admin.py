# encoding: utf-8
__author__ = 'mtianyan'
__date__ = '2018/1/9 0009 08:02'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner




# 创建admin的管理类,这里不再是继承admin，而是继承object
class EmailVerifyRecordAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['code','email','send_type','send_time']


# 创建banner的管理类
class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


# 创建x admin的全局管理器并于view绑定
class BaseSetting(object):
    # 开启主题
    enable_themes = True
    use_bootswatch = True


# Xadmin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "ZMY:课程后台管理站"
    site_footer = "mtianyan's mocc"
    # 收起菜单
    menu_style = 'accordion'



xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)