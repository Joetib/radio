# Generated by Django 3.0.8 on 2020-07-25 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0003_auto_20200724_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]