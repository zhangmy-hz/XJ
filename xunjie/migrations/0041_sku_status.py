# Generated by Django 2.1.15 on 2020-09-13 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0040_auto_20200823_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
