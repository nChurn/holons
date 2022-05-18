from django.db import models
from djmoney.models.fields import MoneyField
from .ray_source import RaySource
from .ray_template import RayTemplate


class UpworkTalent(models.Model):
    """
    @todo: Consider investing some time into refactoring/renaming
    UpworkTalent model to (Ray)Message model
    """

    title = models.CharField(max_length=1024)
    link = models.CharField(max_length=1024)
    description = models.TextField()
    trace_message = models.TextField(blank=True)
    guid = models.CharField(max_length=1024, unique=False)
    ray_source = models.ForeignKey(RaySource,
                                   blank=True,
                                   related_name='messages',
                                   on_delete=models.CASCADE,
                                   default=False)
    pub_date = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=1024, default='')
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_proposed = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    provider = models.TextField(default='upwork')
    templates = models.ManyToManyField(RayTemplate,
                                       blank=True,
                                       related_name='tpl_messages',
                                       default=False)
    budget = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                            blank=True, null=True, default=None)
    rate_from = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                            blank=True, null=True, default=None)
    rate_to = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                            blank=True, null=True, default=None)
    category = models.CharField(max_length=4096, default='')
    skills = models.CharField(max_length=8192, default='')

    @property
    def category_list(self):
        return self.category.lower().split(',')

    @property
    def skills_list(self):
        return self.skills.lower().split(',')

    @property
    def country_clean(self):
        return self.country.lower().strip().replace(' ', '')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
        
    class Meta:
        app_label = 'rays'
        indexes = [
            models.Index(fields=['guid']),
        ]
