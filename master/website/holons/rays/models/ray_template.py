from django.db import models


class RayTemplate(models.Model):

    title = models.CharField(max_length=255)
    bids_total = models.IntegerField(default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    conversions = models.IntegerField(default=0, blank=True, null=True)
    is_archived = models.BooleanField(default=False, null=True)


    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

