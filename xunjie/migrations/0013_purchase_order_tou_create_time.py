# Generated by Django 2.1.15 on 2020-07-25 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0012_sku_classification'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_order_tou',
            name='create_time',
            field=models.CharField(max_length=40, null=True),
        ),
    ]