# encoding: utf-8
__author__ = 'ZMY'
__date__ = '2018/1/9/ 0009 20:10'

from .models import Course,Lesson,Video,CourseResource,BannerCourse
import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0


# Course的管理器
class CourseAdmin(object):
    # inlines 添加数据
    inlines = [LessonInline,CourseResourceInline] # 增加章节和课程资源
    list_display = ['name','desc','detail','degree',
                    'learn_times','students','get_zj_nums','go_to'] # get_zj_nums是章节数

    search_fields = ['name','desc','detail','degree','students']

    list_filter = [ 'name', 'desc','detail',
                    'degree','learn_times','students']
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']        # 排序
    readonly_fields = ['click_nums']  # 只看字段
    exclude = ['fav_nums']            # 不显示的字段
    list_editable = ['degree','desc'] # 列表页直接编辑
    refresh_times = [3,5]             # 自动刷新（里面是秒）
    # detail就是要显示为富文本的字段名
    style_fields = {'detail':'ueditor'}

    def queryset(self):
        # 重载queryset 方法，来过滤出我们想要的数据的
        qs = super(CourseAdmin,self).queryset()
        # 只显示is_banner = True的课程
        qs = qs.filter(is_banner=False)
        return qs

    # 字段联动
    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程会少一个
        obj.save()
        # 确定课程的课程机构存在
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org = course_org).count()
            course_org.save()


# 轮播课程
class BannerCourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','students']
    search_fields = ['name','desc','detail','degree','students']
    list_filter = ['name','desc','detail','degree','learn_times','students']
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        # 重载queryset 方法，来过滤出我们想要的数据的
        qs = super(BannerCourseAdmin,self).queryset()
        # 只显示is_banner = True的课程
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields = ['course','name']

    # __name代表使用外键中的name字段
    list_filter = ['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']


class CourseResourceAdmin(object):
    list_display = ['course','name','download','add_time']
    search_fields = ['course','name','download']
    list_filter = ['course__name','name','download','add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)