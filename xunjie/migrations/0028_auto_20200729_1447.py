# Generated by Django 2.1.15 on 2020-07-29 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0027_purchase_del_fp_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase_order_tou',
            name='note_out',
        ),
        migrations.RemoveField(
            model_name='purchase_order_tou',
            name='order_code_out',
        ),
        migrations.RemoveField(
            model_name='purchase_order_tou',
            name='status_out',
        ),
    ]