# Generated by Django 2.1.15 on 2020-07-28 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0023_auto_20200728_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_del',
            name='item_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='purchase_del',
            name='unit',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]