from django.db import models
import datetime

YEAR_CHOICES = []
for r in range(1960, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


class Genre(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    cover = models.FileField(blank=True)
    link_video = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now=False,  auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title