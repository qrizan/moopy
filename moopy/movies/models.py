from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from comments.models import Comment
from genres.models import Genre
from markdown_deux import markdown
from .utils import get_read_time
import datetime

YEAR_CHOICES = []
for r in range(1960, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


class MovieManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(MovieManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Movie(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True, default='')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    cover = models.FileField(blank=True)
    link_video = models.CharField(max_length=250, blank=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    read_time = models.TimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now=False,  auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = MovieManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movies:movie_detail", kwargs={"slug": self.slug})

    @property
    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        movie = self
        comment = Comment.objects.filter_by_movie(movie)
        return comment

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


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


def pre_save_movie_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_movie_slug(instance)

        # if instance.description:
        #     html_string = instance.get_markdown()
        #     read_time_var = get_read_time(html_string)
        #     instance.read_time = read_time_var

pre_save.connect(pre_save_movie_receiver, sender=Movie)

