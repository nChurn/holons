from django.db import models
from .message_thread import MessageThread


class DirectMessage(models.Model):
    """
    Message in Direct user-to-user Ray

    """

    subject = models.CharField(max_length=1024)
    body = models.TextField()
    type = models.CharField(max_length=128, unique=False)
    message_thread = models.ForeignKey(MessageThread,
                                   blank=True,
                                   null=True,
                                   related_name='messages',
                                   on_delete=models.CASCADE,
                                   default=None)
    pub_date = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    provider = models.TextField(default='holons')

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.subject

    def __unicode__(self):
        return self.subject
