from django import forms
from pagedown.widgets import PagedownWidget
from .models import Movie, Genre


class MovieForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)

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