from django.contrib import admin

# Register your models here.
from .models import Podcast, Category, Series, Advertisement

admin.site.register(Podcast)
admin.site.register(Category)
admin.site.register(Series)
admin.site.register(Advertisement)
