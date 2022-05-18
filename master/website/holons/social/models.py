from django.db import models
from accounts.models import User

class Graph(models.Model):
    user_id = models.IntegerField(unique=True, default=0)
    user = models.ManyToManyField(User, related_name='social', blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
