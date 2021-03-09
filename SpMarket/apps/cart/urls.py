from django.conf.urls import url

from cart.views import AddCartView, CartShowView

app_name = 'cart'
urlpatterns = [

    url(r'^add/$', AddCartView.as_view(), name='添加购物车'),
    url(r'^show/$', CartShowView.as_view(), name='购物车展示'),
]
