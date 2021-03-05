from django.conf.urls import url

from goods.views import IndexView, CategoryView, DetailView

app_name = 'goods'
urlpatterns = [
    # url(r'^login/$', LoginView.as_view(), name="登录"),

    url(r'^goodsindex/$', IndexView.as_view(), name="商品首页"),
    url(r'^detail/(?P<id>\d+)', DetailView.as_view(), name="商品详情"),
    url(r'^list/(?P<cate_id>\d*)_{1}(?P<order>\d?)\.html$', CategoryView.as_view(), name="商品分类列表"),


]
