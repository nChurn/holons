from django.db import models


class ClientStats(models.Model):
    country = models.CharField(max_length=255, default=None, null=True)
    city = models.CharField(max_length=255, default=None, null=True)
    jobs_posted = models.IntegerField(default=None, null=True)
    hire_rate = models.FloatField(default=None, null=True)
    open_jobs = models.IntegerField(default=None, null=True)
    rating = models.FloatField(default=None, null=True)
    reviews_count = models.IntegerField(default=None, null=True)
    guid = models.CharField(max_length=255, unique=False)
    pub_date = models.DateTimeField(default=None, null=True)

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.guid

    def __unicode__(self):
        return self.guid

