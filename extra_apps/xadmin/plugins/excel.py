# # encoding: utf-8
# __author__ = 'ZMY'
# __date__ = '2018/7/10 22:20'
#
# import xadmin
# from xadmin.views import BaseAdminPlugin,ListAdminView
# from django.template import loader
#
#
# # excel格式导入
# class ListImportExcelPlugin(BaseAdminPlugin):
#     import_excel = True
#
#     def init_request(self, *args, **kwargs):
#         return bool(self.import_excel)
#
#     def block_top_toolbar(self,context,nodes):
#         nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html',context_instance=))
#
#
# xadmin.site.register_plugin(ListImportExcelPlugin,ListAdminView)