# Generated by Django 3.0.10 on 2021-05-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycloud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='devs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('date_joined', models.DateTimeField()),
            ],
        ),
    ]