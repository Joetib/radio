from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CommentForm, CreateArticleForm, CreatePodcastForm, CreateNewsForm
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView
from . import models

# Create your views here.


def home_page(request):
    latest_podcasts = models.Podcast.objects.all()[:10]
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else latest_podcasts.first()
    )

    return render(
        request,
        "podcast/home-page.html",
        {"latest_podcasts": latest_podcasts, "featured_podcast": featured_podcast,},
    )


@login_required
def create_podcast(request):
    if request.method == "POST":
        form = CreatePodcastForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.author = request.user
            podcast.save()
            messages.success(request, f"Podcast: {podcast.title} created successfully")
            return redirect(podcast.get_absolute_url())
        else:
            messages.error(
                request,
                f"Error occurred when creating podcast, please try again after fixing the errors",
            )
    else:
        form = CreatePodcastForm()
    return render(request, "podcast/create-podcast.html", {"form": form})


def podcast_detail(request, pk):
    podcast = get_object_or_404(models.Podcast, id=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.podcast = podcast
            comment.save()
            messages.success(request, "Comment created successfully")
        else:
            messages.error(request, "Error creating comment")
    else:
        comment_form = CommentForm()
    recent_podcasts = models.Podcast.objects.exclude(id=podcast.id)[:5]
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else recent_podcasts.first()
    )

    return render(
        request,
        "podcast/podcast-detail.html",
        {
            "comment_form": comment_form,
            "podcast": podcast,
            "featured_podcast": featured_podcast,
            "recent_podcasts": recent_podcasts,
        },
    )


def podcast_list(request):
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    all_podcasts = models.Podcast.objects.all()
    paginator = Paginator(all_podcasts, 12)
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    podcasts = paginator.get_page(page)
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else all_podcasts.first()
    )

    return render(
        request,
        "podcast/podcast-list.html",
        {"featured_podcast": featured_podcast, "podcasts": podcasts,},
    )


def search_podcast(request):
    query = request.GET.get("query", "")

    podcasts_list = models.Podcast.objects.filter(
        Q(title__contains=query)
        | Q(body__contains=query)
        | Q(category__name__contains=query)
        | Q(author__username__contains=query)
    )

    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    paginator = Paginator(podcasts_list, 12)
    print("\n\n\n\n>>> Paginator-details >>> ", type(page), type(paginator.num_pages))

    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1

    podcasts = paginator.get_page(page)
    return render(
        request, "podcast/podcast-list.html", {"query": query, "podcasts": podcasts,},
    )


"""
Articles 
-------------------------------------------------------
"""


@login_required
def create_article(request):
    if request.method == "POST":
        form = CreateArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, f"Article: {article.title} created successfully")
            return redirect(article.get_absolute_url())
        else:
            messages.error(
                request,
                f"Error occurred when creating article, please try again after fixing the errors",
            )
    else:
        form = CreateArticleForm()
    return render(request, "article/create-article.html", {"form": form})


def article_detail(request, pk):
    article = get_object_or_404(models.Article, id=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request, "Comment created successfully")
        else:
            messages.error(request, "Error creating comment")
    else:
        comment_form = CommentForm()
    recent_articles = models.Article.objects.exclude(id=article.id)[:5]
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else models.Podcast.objects.first()
    )

    return render(
        request,
        "article/article-detail.html",
        {
            "comment_form": comment_form,
            "article": article,
            "featured_podcast": featured_podcast,
            "recent_articles": recent_articles,
        },
    )


def article_list(request):
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    all_articles = models.Article.objects.all()
    paginator = Paginator(all_articles, 12)
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    articles = paginator.get_page(page)
    most_liked_articles = models.Article.objects.order_by("liked_by")[:5]
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else models.Podcast.objects.first()
    )
    return render(
        request,
        "article/article-list.html",
        {
            "articles": articles,
            "most_liked_articles": most_liked_articles,
            "featured_podcast": featured_podcast,
        },
    )


def search_article(request):
    query = request.GET.get("query", "")

    articles_list = models.Article.objects.filter(
        Q(title__contains=query)
        | Q(body__contains=query)
        | Q(category__name__contains=query)
        | Q(author__username__contains=query)
    )
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    paginator = Paginator(articles_list, 12)
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    articles = paginator.get_page(page)

    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else models.Podcast.objects.first()
    )
    return render(
        request,
        "article/article-list.html",
        {"query": query, "articles": articles, "featured_podcast": featured_podcast,},
    )


"""
News 
-------------------------------------------------------
"""


@login_required
def create_news(request):
    if request.method == "POST":
        form = CreateNewsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, f"News: {news.title} created successfully")
            return redirect(news.get_absolute_url())
        else:
            messages.error(
                request,
                f"Error occurred when creating news, please try again after fixing the errors",
            )
    else:
        form = CreateNewsForm()
    return render(request, "news/create-news.html", {"form": form})


def news_detail(request, pk):
    news = get_object_or_404(models.News, id=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.save()
            messages.success(request, "Comment created successfully")
        else:
            messages.error(request, "Error creating comment")
    else:
        comment_form = CommentForm()
    recent_news = models.News.objects.exclude(id=news.id)[:5]
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else models.Podcast.objects.first()
    )

    return render(
        request,
        "news/news-detail.html",
        {
            "comment_form": comment_form,
            "news": news,
            "featured_podcast": featured_podcast,
            "recent_news": recent_news,
        },
    )


def news_list(request):
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    all_news = models.News.objects.all()
    paginator = Paginator(all_news, 12)
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    news = paginator.get_page(page)
    most_liked_news = models.News.objects.order_by("liked_by")[:5]
    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else models.Podcast.objects.first()
    )
    return render(
        request,
        "news/news-list.html",
        {
            "news_list": news,
            "most_liked_news": most_liked_news,
            "featured_podcast": featured_podcast,
        },
    )


def search_news(request):
    query = request.GET.get("query", "")

    all_news = models.News.objects.filter(
        Q(title__contains=query)
        | Q(body__contains=query)
        | Q(category__name__contains=query)
        | Q(author__username__contains=query)
    )
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    paginator = Paginator(all_news, 12)
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    news = paginator.get_page(page)

    featured_podcast_qs = models.Podcast.objects.filter(featured=True)
    featured_podcast = (
        featured_podcast_qs.first()
        if featured_podcast_qs.exists()
        else models.Podcast.objects.first()
    )
    return render(
        request,
        "news/news-list.html",
        {"query": query, "news_list": news, "featured_podcast": featured_podcast,},
    )

