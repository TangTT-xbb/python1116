from django.conf.urls import url

from order.views import ConfirmOrderView, ShowOrder, Pay

app_name = 'order'
urlpatterns = [

    url(r'^confirm/$',ConfirmOrderView.as_view(),name='确认订单'),
    url(r'^order/$',ShowOrder.as_view(),name='确认支付'),
    url(r'^pay/$',Pay.as_view(),name='支付结果'),

]