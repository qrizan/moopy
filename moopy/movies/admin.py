from django.contrib import admin
from .models import Movie


class MovieModelAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "updated", "created"]
    list_display_links = ["title"]
    list_filter = ["genre", "created"]
    search_fields = ["title", "description"]

    class Meta:
        model = Movie


admin.site.register(Movie, MovieModelAdmin)
