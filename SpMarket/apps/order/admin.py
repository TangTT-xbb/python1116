from django.contrib import admin

# Register your models here.
from order.models import Transport, Payment


# admin.site.register(Transport)
# admin.site.unregister(Transport)

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    # 自定义后台
    list_display = ['id', 'name', 'price']
    list_display_links = ['id', 'name', 'price']


admin.site.register(Payment)
