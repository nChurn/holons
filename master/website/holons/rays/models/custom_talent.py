from django.db import models


class CustomTalent(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    guid = models.CharField(max_length=255, unique=False, blank=True)
    ray_source = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

