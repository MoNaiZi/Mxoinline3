# encoding:utf-8
__author = 'mtianyan'
__date__ = '2018/5/19 8:35'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


# 用户更改图像
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

# 验证码form & 注册表单form
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    # 应用验证码
    captcha = CaptchaField()


# 注册验证码实现
class ForgetForm(forms.Form):
    # email与前端name需保持一致
    email = forms.EmailField(required=True)
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不对邮箱密码做验证
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


# 重置密码form实现
class ModifyPwdForm(forms.Form):
    # 密码不能小于5位
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)


# 用于个人中心修改个人信息
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birthday','address','mobile']