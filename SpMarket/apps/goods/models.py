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
