from django.db import models
from .message_thread import MessageThread

class Ray(models.Model):
    """
    Thread of Direct Ray messages
    shared between users

    """

    message_thread = models.ManyToManyField(MessageThread,
                                   blank=True,
                                   related_name='ray',
                                   default=None)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, default=None)

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)
