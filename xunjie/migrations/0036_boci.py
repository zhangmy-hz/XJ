# Generated by Django 2.1.15 on 2020-08-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xunjie', '0035_sale_first_api'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boci',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boci', models.CharField(default='', max_length=20, null=True)),
                ('status', models.CharField(max_length=10, null=True)),
                ('note', models.CharField(max_length=100, null=True)),
                ('create_time', models.CharField(max_length=40, null=True)),
            ],
        ),
    ]