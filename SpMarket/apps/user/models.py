from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from db.base_model import BaseModel


class SpUser(BaseModel):
    """
    用户表
    """
    sex_choice = (
        (1,'男'),
        (2,'女'),
    )
    phone = models.CharField(max_length= 11,
                             verbose_name='手机号码',
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$','请填写正确的手机号码')
                             ])
    nickname = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name='昵称',
                                )
    password = models.CharField(max_length=32,
                                verbose_name='密码')
    gender = models.SmallIntegerField(choices=sex_choice,
                                      default=1,
                                      verbose_name='性别')
    school_name = models.CharField(max_length=50,
                                   null=True,
                                   blank=True,
                                   verbose_name='学校',
                                   )
    hometown = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name='家乡',
                                )
    birth_of_date = models.DateField(null=True,
                                         blank=True,
                                         verbose_name='出生日期',)
    address = models.CharField(max_length=50,
                               null=True,
                               blank=True,
                               verbose_name='地址',
                               )

    # 设置头像字段
    head = models.ImageField(upload_to='head/%Y%m',default='head/memtx.png',verbose_name='用户头像')

    # 定义额外字段
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')


    def __str__(self):
        return self.phone

    class Meta:
        db_table= "sp_user"
        verbose_name = '用户管理'
        verbose_name_plural=verbose_name