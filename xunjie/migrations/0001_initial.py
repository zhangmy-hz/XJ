# Generated by Django 2.1.15 on 2020-07-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='quanxian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_name', models.CharField(max_length=20)),
                ('jon_code', models.CharField(max_length=20)),
                ('job_name', models.CharField(max_length=20)),
                ('level', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=40)),
                ('role_explain', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roles_Del',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=40)),
                ('code_name', models.CharField(default='null', max_length=20)),
                ('jon_code', models.CharField(default='null', max_length=20)),
                ('job_name', models.CharField(default='null', max_length=20)),
                ('level', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=40, null=True)),
                ('update_time', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nameid', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20, null=True)),
                ('iphone', models.CharField(max_length=20, null=True)),
                ('jiaose', models.CharField(max_length=20, null=True)),
                ('status', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=20, null=True)),
                ('role', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]