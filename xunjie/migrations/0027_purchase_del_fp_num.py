# Generated by Django 2.1.15 on 2020-07-29 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0026_auto_20200729_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_del',
            name='fp_num',
            field=models.IntegerField(default=0),
        ),
    ]
