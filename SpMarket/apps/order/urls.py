from django.conf.urls import url

from order.views import ConfirmOrderView

app_name = 'order'
urlpatterns = [

    url(r'^add/$',ConfirmOrderView.as_view(),name='确认订单'),

]