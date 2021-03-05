from django.conf.urls import url

from cart.views import AddCartView
app_name = 'cart'
urlpatterns = [

    url(r'^add/$',AddCartView.as_view(),name='添加购物车'),
]