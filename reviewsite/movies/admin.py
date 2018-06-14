from django.contrib import admin
from .models import MovieModel, MovieReview


# Register your models here.
admin.site.register(MovieModel)
admin.site.register(MovieReview)

