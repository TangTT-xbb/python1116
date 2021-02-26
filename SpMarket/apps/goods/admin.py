
from django.contrib import admin

# Register your models here.
from goods.models import GoodsSPU, GoodsSKU, Category, Unit

admin.site.register(GoodsSPU)
admin.site.register(GoodsSKU)
admin.site.register(Category)
admin.site.register(Unit)
