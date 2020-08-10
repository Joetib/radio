from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category: {self.name}>"


class Series(models.Model):
    title = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Series: {self.title[:30]}>"

    def get_next_podcast(self, podcast_id):
        next_podcast = self.podcasts.filter(id__gt=podcast_id)
        if next_podcast.exists():
            return next_podcast.first()
        return None

    def get_prev_podcast(self, podcast_id):
        prev_podcast = self.podcasts.filter(id__lt=podcast_id)
        if prev_podcast.exists():
            return prev_podcast.last()
        return None

    def get_next_podcast(self, article_id):
        next_article = self.articles.filter(id__gt=article_id)
        if next_article.exists():
            return next_article.first()
        return None

    def get_prev_article(self, article_id):
        prev_article = self.articles.filter(id__lt=article_id)
        if prev_article.exists():
            return prev_article.last()
        return None


class Podcast(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_podcasts"
    )
    category = models.ForeignKey(
        Category, related_name="podcast", on_delete=models.CASCADE
    )
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, related_name="podcasts", blank=True, null=True
    )
    title = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to="podcast/picture/%Y/%m/")
    featured = models.BooleanField(default=False)
    audio = models.FileField(upload_to="podcast/audio/%Y/%m/")
    body = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="liked_podcasts")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("podcast:podcast-detail", kwargs={"pk": self.id})

    def get_previous_podcast(self):
        if self.series:
            podcast = self.series.get_prev_podcast(self.id)
            if podcast:
                return podcast
        podcast_qs = Podcast.objects.filter(id__lt=self.id)
        if podcast_qs.exists():
            return podcast_qs.last()
        return None

    def get_next_podcast(self):
        if self.series:
            podcast = self.series.get_next_podcast(self.id)
            if podcast:
                return podcast
        podcast_qs = Podcast.objects.filter(id__gt=self.id)
        if podcast_qs.exists():
            return podcast_qs.first()
        return None


class Article(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_articles"
    )
    category = models.ForeignKey(
        Category, related_name="article", on_delete=models.CASCADE
    )
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, related_name="articles", blank=True, null=True
    )
    title = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to="article/picture/%Y/%m/")
    body = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="liked_articles")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Article: {self.title}>"

    def get_absolute_url(self):
        return reverse("podcast:article-detail", kwargs={"pk": self.id})

    def get_previous_article(self):
        if self.series:
            article = self.series.get_prev_article(self.id)
            if article:
                return article
        article_qs = Article.objects.filter(id__lt=self.id)
        if article_qs.exists():
            return article_qs.last()
        return None

    def get_next_article(self):
        if self.series:
            article = self.series.get_next_article(self.id)
            if article:
                return article
        article_qs = Article.objects.filter(id__gt=self.id)
        if article_qs.exists():
            return article_qs.first()
        return None


class News(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_news"
    )
    category = models.ForeignKey(
        Category, related_name="news", on_delete=models.CASCADE
    )
    series = models.ForeignKey(
        Series, on_delete=models.CASCADE, related_name="news_set", blank=True, null=True
    )
    title = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to="news/picture/%Y/%m/")
    body = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="liked_news")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Article: {self.title}>"

    def get_absolute_url(self):
        return reverse("podcast:news-detail", kwargs={"pk": self.id})


class Comment(models.Model):
    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="comments", blank=True, null=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments

    def __repr__(self):
        return f"<Comment: {self.comment[:30]}>"


class Advertisement(models.Model):
    title = models.CharField(max_length=500)
    picture = models.ImageField(upload_to="advertisement/%Y/%m/", blank=True, null=True)
    end_date = models.DateField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Advertisement: {self.title[:50]}>"

