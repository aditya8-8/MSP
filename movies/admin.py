from django.contrib import admin
from .models import Movies


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'Predicted_Rating',)
    list_display_links = ('name',)
    search_fields = ('id', 'name', 'year',)
    list_per_page = 10
    ordering = ('id',)

admin.site.register(Movies, MovieAdmin)

