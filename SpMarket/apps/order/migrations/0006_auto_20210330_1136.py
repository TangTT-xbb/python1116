# Generated by Django 3.1.3 on 2021-03-30 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_payment_id_tuijian'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='id_tuijian',
            new_name='is_tuijian',
        ),
    ]
