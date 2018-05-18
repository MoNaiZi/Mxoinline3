from django.shortcuts import render
from django.contrib.auth import authenticate,login

#自定义authenticate方法
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
#并集运算
from django.db.models import Q



def user_login(request):
    if request.method == 'POST':
        #取不到值时为空
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        # 成功返回user对象，失败返回null
        user = authenticate(username = user_name,password = pass_word)
    
        if user is not None:
            login(request,user)
            return render(request,'index.html')

        else:
            return render(request,'login.html')
        
    elif request.method == 'GET':
        return render(request,'login.html')

    else:
        return render(request, 'login.html', {"msg": "用户名或密码错误！"})



#实现用户名邮箱均可登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能一个。Q为使用并集查询
            user = UserProfile.objects.get(Q(username = username)|Q(email = username))

            # django的后台中密码加密：所以不能password == passowrd
            # UserProfile继承的AbstractUser中有def check_passoword(self,raw_password):

            if user.check_password(password):
                return user
                
        except Exception as e:
            return None