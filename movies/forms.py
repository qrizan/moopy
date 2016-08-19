from django import forms
from .models import Movie, Genre


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "genre",
            "year",
            "cover",
            "draft",
            "publish",
            "link_video"
        ]


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = [
            "name",
            "draft",
            "publish"
        ]