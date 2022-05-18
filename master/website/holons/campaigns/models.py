from django.db import models
from rays.models.ray_template import RayTemplate
from accounts.models import User


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    templates = models.ManyToManyField(RayTemplate, related_name='campaigns', blank=True)
    owner = models.ManyToManyField(User, related_name='campaigns', blank=True)
    beneficiary = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return self.title

class Log(models.Model):
    event_type = models.CharField(max_length=255)
    template = models.ForeignKey(RayTemplate,
                                related_name='logs',
                                blank=True,
                                on_delete=models.CASCADE,
                                default=False)
    event_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.event_type + ' ' + str(self.event_date)
