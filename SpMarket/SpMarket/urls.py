"""SpMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from SpMarket import settings
from goods.views import IndexView

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  # 添加第三方插件
                  # 全文搜索框架
                  url(r'^search/', include(('haystack.urls', "haystack"), namespace='search')),

                  url(r'^cart/', include('cart.urls', namespace='cart')),
                  url(r'^user/', include('user.urls', namespace='user')),
                  # url(r'^order/', include('order.urls',namespace='order')),
                  url(r'^goods/', include('goods.urls', namespace='goods')),
                  url(r'^order/', include('order.urls', namespace='order')),
                  # 上传部件自动调用的上传地址
                  url(r'^ckeditor/', include("ckeditor_uploader.urls")),
                  url(r'^$', IndexView.as_view()),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
