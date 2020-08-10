from podcast.views import home_page
from django.urls import path
from . import views

app_name = "podcast"

urlpatterns = [
    path('', views.home_page, name="home-page"),
    path('podcast/',views.podcast_list, name="podcast-list"),
    path('podcast/search/',views.search_podcast, name="podcast-search"),
    path('podcast/create/',views.create_podcast, name="create-podcast"),
    path('podcast/detail/<int:pk>/',views.podcast_detail, name="podcast-detail"),

    # Articles 

    path('article/',views.article_list, name="article-list"),
    path('article/search/',views.search_article, name="article-search"),
    path('article/create/',views.create_article, name="create-article"),
    path('article/detail/<int:pk>/',views.article_detail, name="article-detail"),


    # News 

    path('news/',views.news_list, name="news-list"),
    path('news/search/',views.search_news, name="news-search"),
    path('news/create/',views.create_news, name="create-news"),
    path('news/detail/<int:pk>/',views.news_detail, name="news-detail"),

    
]