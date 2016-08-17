from django.contrib import admin
from .models import Movie, Genre


class MovieModelAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "updated", "created"]
    list_display_links = ["title"]
    list_filter = ["genre", "created"]
    search_fields = ["title", "description"]

    class Meta:
        model = Movie


class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["updated"]
    list_editable = ["name"]
    list_filter = ["created"]

    class Meta:
        model = Genre

admin.site.register(Movie, MovieModelAdmin)
admin.site.register(Genre, GenreModelAdmin)
