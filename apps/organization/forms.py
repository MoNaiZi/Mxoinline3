# encoding: utf-8
__author__ = 'ZMY'
__date__ = '2018/5/31 7:50'
from django import forms

from operation.models import UserAsk
import re


# 普通版本的form(form会对字段先做验证，然后保存到数据库中）
# 可以看到我们的forms和我们的model中有很多内容是一样的。我们要重复利用代码勒？
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone = forms.CharField(required=True,max_length=11,min_length=11)
#     course_name = forms.CharField(required=True,min_length=5,max_length=50)



# 进阶版本的modelform:它可以向model一样save
class AnotherUserForm(forms.ModelForm):
    # 继承之余还可以新增字段

    # 是由那个model转换的
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']


# 手机号的正则表达式验证
def clean_mobile(self):
    mobile = self.cleaned_data['mobile']
    REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
    p = re.compile(REGEX_MOBILE)
    if p.match(mobile):
        return mobile
    else:
        raise forms.ValidationError('手机号码非法',code='mobile_invalid')