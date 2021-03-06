# Generated by Django 3.1.3 on 2021-03-22 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20210304_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('img_url', models.ImageField(upload_to='goods_gallery/%Y%m/%d', verbose_name='相册图片地址')),
                ('goods_sku', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='goods.goodssku', verbose_name='商品SKU')),
            ],
            options={
                'verbose_name': '商品相册管理',
                'verbose_name_plural': '商品相册管理',
                'db_table': 'Gallery',
            },
        ),
    ]
