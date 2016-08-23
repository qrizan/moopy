from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models


class CommentManager(models.Manager):
    def all(self):
        comment = super(CommentManager, self).filter(parent=None)
        return comment

    def filter_by_movie(self, movie):
        content_type = ContentType.objects.get_for_model(movie.__class__)
        object_id = movie.id
        comment = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
        return comment


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True)

    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("comments:comment_thread", kwargs={"id": self.id})

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True