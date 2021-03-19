from django.contrib import admin

# Register your models here.
from goods.models import GoodsSPU, GoodsSKU, Category, Unit, Gallery

# 商品SKU
"""
注册方式:
admin.site.register(模型类)

装饰器形式注册
@admin.register(模型类)
class XxxAdmin(admin.ModelAdmin):
    # 自定义后显示的类
"""


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 自定义后台
    list_display = ['id', 'cate_name', 'brief', 'order', 'update_time']
    list_display_links = ['id', 'cate_name', 'brief']


admin.site.register(GoodsSPU)
admin.site.register(Unit)


# admin.site.unregister(GoodsSKU)
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 2


@admin.register(GoodsSKU)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_display = ["id", 'sku_name', 'show_logo', 'price', 'unit', 'stock', 'sale_num', 'is_on_sale', 'category']
    list_display_links = ["id", 'sku_name', 'price']

    list_editable = ['is_on_sale']

    search_fields = ['sku_name', 'price', 'sale_num']
    # inlines = [
    #     GalleryInline,
    # ]
