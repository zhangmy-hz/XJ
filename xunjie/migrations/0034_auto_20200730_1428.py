# Generated by Django 2.1.15 on 2020-07-30 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0033_auto_20200730_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='status',
            new_name='stocks_tatus',
        ),
    ]
