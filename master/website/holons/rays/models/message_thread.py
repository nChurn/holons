from django.db import models


class MessageThread(models.Model):
    """
    Thread of Direct Ray messages
    shared between users

    """

    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)
