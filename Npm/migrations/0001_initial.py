# Generated by Django 2.2.1 on 2019-05-26 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NpmPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
            ],
        ),
    ]
