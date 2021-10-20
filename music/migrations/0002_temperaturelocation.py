# Generated by Django 3.2.7 on 2021-09-29 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemperatureLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=128)),
                ('style', models.CharField(max_length=32)),
                ('last_update_time', models.DateTimeField()),
            ],
        ),
    ]
