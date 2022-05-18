from django.db import models
from .upwork_talent import UpworkTalent


class MessageAssigned(models.Model):

    message = models.ForeignKey(UpworkTalent,
                                blank=True,
                                on_delete=models.CASCADE,
                                default=False)
    owner = models.IntegerField(blank=True, default=None)
    assignee = models.IntegerField(blank=True, default=None)

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.message.title

    def __unicode__(self):
        return self.message.title
