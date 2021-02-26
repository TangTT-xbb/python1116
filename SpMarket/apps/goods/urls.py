from django.conf.urls import url

from goods.views import goodsindex, goodsdetail, category

app_name = 'goods'
urlpatterns = [
    # url(r'^login/$', LoginView.as_view(), name="登录"),

    url(r'^goodsindex/$', goodsindex, name="商品首页"),
    url(r'^goodsdetail/(?P<q>\d)', goodsdetail, name="商品详情"),
    url(r'^goodslist/$', category, name="商品分类列表"),


]
