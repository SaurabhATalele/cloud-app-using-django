# Generated by Django 3.2 on 2021-04-29 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=10)),
                ('loc', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=40)),
                ('filesize', models.IntegerField()),
                ('date_created', models.DateField()),
                ('host', models.CharField(max_length=100)),
            ],
        ),
    ]
