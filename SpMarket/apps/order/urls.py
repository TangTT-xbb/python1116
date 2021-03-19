from django.conf.urls import url

from order.views import ConfirmOrderView, ShowOrder

app_name = 'order'
urlpatterns = [

    url(r'^confirm/$',ConfirmOrderView.as_view(),name='确认订单'),
    url(r'^order/$',ShowOrder.as_view(),name='确认支付'),

]