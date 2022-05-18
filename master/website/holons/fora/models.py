from django.db import models


class ForaChannel(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField(default='')
    description = models.TextField(default='')
    is_tech = models.BooleanField(default=False)
    is_development = models.BooleanField(default=False)
    is_news = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_coding = models.BooleanField(default=False)
    is_humor = models.BooleanField(default=False)
    is_crypto = models.BooleanField(default=False)
    is_design = models.BooleanField(default=False)
    is_marketing = models.BooleanField(default=False)
    is_data = models.BooleanField(default=False)
    is_science = models.BooleanField(default=False)
    is_jobs = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
