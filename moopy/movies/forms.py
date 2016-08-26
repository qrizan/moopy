from django import forms
from pagedown.widgets import PagedownWidget
from .models import Movie


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
