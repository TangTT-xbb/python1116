# Generated by Django 3.1.3 on 2021-03-30 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20210325_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='id_tuijian',
            field=models.BooleanField(default=False, verbose_name='是否推荐'),
        ),
    ]