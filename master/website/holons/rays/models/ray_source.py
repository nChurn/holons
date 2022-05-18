from django.db import models


class RaySource(models.Model):

    title = models.CharField(max_length=255)
    link = models.TextField(default='')
    stop_words = models.TextField(default='', null=True)
    key_words = models.TextField(default='',  null=True)
    title_filter = models.TextField(default='')
    skills_filter = models.TextField(default='')
    category_filter = models.TextField(default='')
    is_active = models.BooleanField(default=True)
    is_budget_empty_ok = models.BooleanField(default=True, null=True)
    budget_rate = models.IntegerField(default=0, blank=True, null=True)
    budget_fixed = models.IntegerField(default=0, blank=True, null=True)
    provider = models.TextField(default='upwork')

    @property
    def title_filter_list(self):
        return self.title_filter.lower().split(',')

    @property
    def category_filter_list(self):
        return self.category_filter.lower().split(',')

    @property
    def skills_filter_list(self):
        return self.skills_filter.lower().split(',')

    @property
    def key_words_list(self):
        if type(self.key_words) is str:
          return self.key_words.lower().replace(' ', '').split(',')
        else:
          return ['']


    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

