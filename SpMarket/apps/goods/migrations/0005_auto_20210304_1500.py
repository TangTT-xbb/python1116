# Generated by Django 3.1.3 on 2021-03-04 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20210304_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodssku',
            old_name='sales',
            new_name='sale_num',
        ),
    ]
