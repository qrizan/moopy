from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

import datetime

YEAR_CHOICES = []
for r in range(1960, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))

# over reading from Genre.objects.all()


class GenreManager(models.Manager):
    def active(self, *args, **kwargs):
        # Genre.objects.all() = super(GenreManager, self).all()
        return super(GenreManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class MovieManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(MovieManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,blank=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = GenreManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("movies:genre_detail", kwargs={"slug": self.slug})


class Movie(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    cover = models.FileField(blank=True)
    link_video = models.CharField(max_length=250, blank=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created = models.DateTimeField(auto_now=False,  auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = MovieManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movies:movie_detail", kwargs={"slug": self.slug})


def create_genre_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Genre.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_genre_slug(instance, new_slug=new_slug)
    return slug


def create_movie_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Movie.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_movie_slug(instance, new_slug=new_slug)
    return slug


def pre_save_genre_receiver(sender, instance, *args, **kwargs):
    # slug = slugify(instance.name)
    # exist = Genre.objects.filter(slug=slug).exists()
    # if exist:
    #     slug = "%s-%s" %(slug, instance.id)
    # instance.slug = slug
    if not instance.slug:
        instance.slug = create_genre_slug(instance)


def pre_save_movie_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_movie_slug(instance)


pre_save.connect(pre_save_genre_receiver, sender=Genre)

pre_save.connect(pre_save_movie_receiver, sender=Movie)


