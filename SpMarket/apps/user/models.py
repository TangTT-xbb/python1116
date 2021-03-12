from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from db.base_model import BaseModel


class SpUser(BaseModel):
    """
    用户表
    """
    sex_choice = (
        (1, '男'),
        (2, '女'),
    )
    phone = models.CharField(max_length=11,
                             verbose_name='手机号码',
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', '请填写正确的手机号码')
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
                                     verbose_name='出生日期', )
    address = models.CharField(max_length=50,
                               null=True,
                               blank=True,
                               verbose_name='地址',
                               )

    # 设置头像字段
    head = models.ImageField(upload_to='head/%Y%m', default='head/memtx.png', verbose_name='用户头像')

    # 定义额外字段
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "sp_user"
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


class UserAddress(BaseModel):
    """用户收货地址管理"""
    user = models.ForeignKey(to="SpUser", verbose_name="创建人", on_delete=models.CASCADE)
    username = models.CharField(verbose_name="收货人", max_length=50)
    phone = models.CharField(verbose_name="收货人电话", max_length=11, validators=[
        RegexValidator(r'^1[3-9]\d{9}$', '请填写正确的手机号码')
    ])
    hcity = models.CharField(verbose_name="省", max_length=100)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, null=True)
    harea = models.CharField(verbose_name="区", max_length=100, blank=True, null=True)
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False, blank=True)

    class Meta:
        db_table = "user_address"
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}:{}".format(self.username, self.phone)
