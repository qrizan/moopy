from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone


class GenreManager(models.Manager):
    def active(self, *args, **kwargs):
        # Genre.objects.all() = super(GenreManager, self).all()
        return super(GenreManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = GenreManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genres:genre_detail", kwargs={"slug": self.slug})


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


def pre_save_genre_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_genre_slug(instance)

pre_save.connect(pre_save_genre_receiver, sender=Genre)