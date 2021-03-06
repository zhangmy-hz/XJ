# Generated by Django 2.1.15 on 2020-07-29 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0028_auto_20200729_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale_Del',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=20)),
                ('item_code', models.CharField(max_length=20)),
                ('item_name', models.CharField(max_length=200, null=True)),
                ('item_gg', models.CharField(default='', max_length=200, null=True)),
                ('unit', models.CharField(default='', max_length=20, null=True)),
                ('num', models.IntegerField(default=0)),
                ('sure_num', models.IntegerField(default=0)),
                ('note', models.CharField(default='', max_length=200, null=True)),
                ('boci', models.CharField(default='', max_length=20, null=True)),
                ('date', models.CharField(default='', max_length=40, null=True)),
                ('store_code', models.CharField(default='', max_length=20, null=True)),
                ('store_name', models.CharField(default='', max_length=40, null=True)),
                ('status', models.CharField(default='待下发', max_length=10, null=True)),
                ('biaozhi', models.CharField(max_length=40, null=True)),
                ('pur_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sale_order_tou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=20)),
                ('boci', models.CharField(max_length=20, null=True)),
                ('date', models.CharField(max_length=40, null=True)),
                ('create_time', models.CharField(max_length=40, null=True)),
                ('store_code', models.CharField(max_length=20)),
                ('store_name', models.CharField(max_length=40, null=True)),
                ('note', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(default='待下发', max_length=10, null=True)),
                ('biaozhi', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='purchase_del',
            name='fp_num',
        ),
        migrations.RemoveField(
            model_name='purchase_del',
            name='note_out',
        ),
        migrations.RemoveField(
            model_name='purchase_del',
            name='order_code_out',
        ),
        migrations.RemoveField(
            model_name='purchase_del',
            name='out_num',
        ),
        migrations.RemoveField(
            model_name='purchase_del',
            name='status_out',
        ),
    ]
