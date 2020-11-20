from django.conf.urls import url

from user.views import LoginView

urlpatterns = [
 url(r'^login/$',LoginView.as_view(),name="登录"),
]