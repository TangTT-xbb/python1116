from SpMarket import settings

from django.utils.safestring import mark_safe


from django.db import models

# Create your models here.
# 商品分类表 （Id 分类名 分类简介 添加时间 修改时间 是否删除）
# 商品SKU表 （Id 商品名 简介 价格 单位 库存 销量 logo地址 是否上架 商品分类ID 商品SPU_id 添加时间 修改时间 是否删除）
# 商品SPU表 （Id 名称 详情）
# 商品相册 （Id 图片地址 商品SKU_id 添加时间 修改时间 是否删除）
# 商品单位表 （Id 单位名(斤，箱) 添加时间 修改时间 是否删除）

# 首页活动表（ID 名称 图片地址 url地址）
# 首页轮播商品表（ID 名称 商品SKU_id 图片地址 排序(order) 添加时间 修改时间 是否删除）
# 首页活动专区（ID 名称 描述 排序 是否上架 添加时间 修改时间 是否删除）
# 首页专区活动商品表（ID 专区ID 商品SKU_id 添加时间 修改时间 是否删除）

# 导入ckeditor上富文本编辑器自带字段
from ckeditor_uploader.fields import RichTextUploadingField

from db.base_model import BaseModel


class GoodsSPU(BaseModel):
    """
        商品SPU表
    """
    spu_name = models.CharField(verbose_name='商品SPU名称',
                                max_length=20,
                                )
    # 使用ckeditor为我们提供的字段，不用重新迁移就可以
    content = RichTextUploadingField(verbose_name="商品详情")

    def __str__(self):
        return self.spu_name

    class Meta:
        db_table = "goods_SPU"
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name


# 商品分类表 （Id 分类名 分类简介 添加时间 修改时间 是否删除）

class Category(BaseModel):
    """商品分类表"""
    cate_name = models.CharField(verbose_name='商品分类名',
                                 max_length=20)
    brief = RichTextUploadingField(verbose_name="商品分类简介")
    order = models.SmallIntegerField(default=0, verbose_name="排序")

    def __str__(self):
        return self.cate_name

    class Meta:
        db_table = "Category"
        verbose_name = "商品分类管理"
        verbose_name_plural = verbose_name


# 商品SKU表 （Id 商品名 简介 价格 单位 库存 销量 logo地址 是否上架 商品分类ID 商品SPU_id 添加时间 修改时间 是否删除）
class GoodsSKU(BaseModel):
    """
        商品SPU表
    """
    is_on_sale_choices = (
        (False, '不上架'),
        (True, '上架'),)
    sku_name = models.CharField(verbose_name='商品SKU名称',
                                max_length=20,
                                )
    # 使用ckeditor为我们提供的字段，不用重新迁移就可以
    brief = RichTextUploadingField(verbose_name="商品简介")
    # 设置了精度的十进制数字
    # models.DecimalField(max_digits=None, decimal_places=None[, **options])
    # 使用Decimal实例表示固定精度的十进制数的字段。它有两个必须的参数：
    # max_digits：数字允许的最大位数
    # decimal_places：小数的最大位数
    price = models.DecimalField(verbose_name='商品价格',
                                max_digits=9,
                                decimal_places=2,
                                default=0)

    unit = models.ForeignKey(to="Unit", on_delete=models.DO_NOTHING, verbose_name='商品单位')
    stock = models.IntegerField(verbose_name='库存', default=0)
    sale_num = models.IntegerField(verbose_name='销量', default=0)
    # logo_url = models.URLField(verbose_name='logo地址')
    # 默认相册中的第一张图片作为封面照片
    logo = models.ImageField(verbose_name='封面照片',
                             upload_to='goods/%Y%m/%d')
    def show_logo(self):
        return mark_safe("<img style='width:50px' src='{}{}'/>".format(settings.MEDIA_URL,self.logo))
    show_logo.short_description = "LOGO"
    show_logo.allow_tags = True
    is_on_sale = models.BooleanField(verbose_name='商品是否上架',
                                     choices=is_on_sale_choices,
                                     default=False)
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='商品分类ID',
                                 )
    goods_spu = models.ForeignKey(GoodsSPU,
                                  on_delete=models.CASCADE,
                                  verbose_name='商品的SPU',
                                  )

    def __str__(self):
        return self.sku_name

    class Meta:
        db_table = "goods_SKU"
        verbose_name = "商品SKU管理"
        verbose_name_plural = verbose_name


# 商品单位表 （Id 单位名(斤，箱) 添加时间 修改时间 是否删除）
class Unit(BaseModel):
    unit_name = models.CharField(verbose_name='单位名',
                                 max_length=10)

    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = "Unit"
        verbose_name = "商品单位"
        verbose_name_plural = verbose_name


class Gallery(BaseModel):
    """
       商品相册
    """
    img_url = models.ImageField(verbose_name='相册图片地址',
                                upload_to='goods_gallery/%Y%m/%d'
                                )

    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU",on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "Gallery"
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品相册:{}".format(self.img_url.name)
