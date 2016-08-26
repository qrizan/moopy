from django.contrib import admin
from .models import Genre


class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["updated"]
    list_editable = ["name"]
    list_filter = ["created"]

    class Meta:
        model = Genre

admin.site.register(Genre, GenreModelAdmin)