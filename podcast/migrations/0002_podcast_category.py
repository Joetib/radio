# Generated by Django 3.0.8 on 2020-07-24 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='podcast', to='podcast.Category'),
            preserve_default=False,
        ),
    ]
