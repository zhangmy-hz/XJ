# Generated by Django 2.1.15 on 2020-07-30 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0031_stock_order_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]