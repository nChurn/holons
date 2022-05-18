from django.db import models
from accounts.models import User

class Token(models.Model):
    value = models.CharField(max_length=255, default='')
    token_type = models.CharField(max_length=255, default='invitation')
    created_at = models.DateTimeField(auto_now=True)
    valid_until = models.DateTimeField(blank=True, null=True, default=None)
    issuer = models.ManyToManyField(User, related_name='invitation_token', blank=True)
    used_by = models.ManyToManyField(User, related_name='invitation_used', blank=True)
    status = models.CharField(max_length=255)
    number_of_uses_left = models.IntegerField(null=True, default=None)

    def __unicode__(self):
        return self.value + ' : ' + self.token_type 
  
