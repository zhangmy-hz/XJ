# Generated by Django 2.1.15 on 2020-07-26 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0014_auto_20200725_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_del',
            name='biaozhi',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='purchase_order_tou',
            name='biaozhi',
            field=models.CharField(max_length=40, null=True),
        ),
    ]