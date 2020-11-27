from django.conf.urls import url

from user.views import LoginView, RegisterView, MemberView, ForgetpwdView

app_name = 'user'
urlpatterns = [
 url(r'^login/$',LoginView.as_view(),name="登录"),
 url(r'^register/$',RegisterView.as_view(),name="注册"),
 url(r'^member/$',MemberView.as_view(),name="个人中心"),
 url(r'^forgetpwd/$',ForgetpwdView.as_view(),name="忘记密码"),

]