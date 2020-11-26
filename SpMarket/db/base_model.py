from django.db import models


class BaseModel(models.Model):
    """基础模型类，让所有的模型类都能继承该类"""
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        # 说明这是一个抽象模型类，不会被迁移
        # Meta中abstract用于声明该类为抽象类只能用于继承
        # 之后所有的模型都继承BaseModel类
        abstract = True
