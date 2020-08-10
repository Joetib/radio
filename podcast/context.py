from .models import Advertisement, Category
from datetime import date

def get_category_context(*args, **kwargs):
    return {
        "categories": Category.objects.all(),
    }

def get_advertisement_context(*args, **kwargs):
    return {
        "adverts": Advertisement.objects.filter(end_date__gte = date.today())
    }