# Generated by Django 3.0.8 on 2020-08-01 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcast', '0005_article_articlecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('picture', models.ImageField(upload_to='news/picture/%Y/%m/')),
                ('body', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_news', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='podcast.Category')),
                ('liked_by', models.ManyToManyField(related_name='liked_news', to=settings.AUTH_USER_MODEL)),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news_set', to='podcast.Series')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='podcast.Article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='podcast',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='podcast.Podcast'),
        ),
        migrations.DeleteModel(
            name='ArticleComment',
        ),
        migrations.AddField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='podcast.News'),
        ),
    ]
