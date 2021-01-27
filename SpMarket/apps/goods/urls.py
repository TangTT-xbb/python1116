from django.conf.urls import url

from goods.views import goodsindexview

app_name = 'goods'
urlpatterns = [
    # url(r'^login/$', LoginView.as_view(), name="登录"),

    url(r'^goodsindex/$', goodsindexview, name="商品首页"),


]
