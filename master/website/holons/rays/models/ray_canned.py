import string
import random

from django.db import models
from django.utils.text import slugify


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

class RayCanned(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
          value = self.title
          self.slug = slugify(value, allow_unicode=True) + '-' + rand_slug()
        else:
          self.slug = self.slug
        super().save(*args, **kwargs)

