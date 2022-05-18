from django.db import models
from accounts.models import User

class BusinessEntity(models.Model):
    name = models.CharField(max_length=255, unique=False, default="")
    owner = models.ManyToManyField(User, related_name='entities', blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


from purpose.models import Context

class CostTag(models.Model):
    name = models.CharField(max_length=255, unique=False)

    context = models.ForeignKey(
        Context, on_delete=models.CASCADE, related_name='costs_tags',
        default=None, null=True, blank=True,
    )
    owner = models.ForeignKey(User, related_name='costs_tags', on_delete=models.CASCADE, blank=True)

    @property
    def uses_count(self):
        return self.fixed_costs.count()

class FixedCost(models.Model):
    name = models.CharField(max_length=400, unique=False)
    amount = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    context = models.ForeignKey(
        Context, on_delete=models.CASCADE, related_name='fixed_costs',
        default=None, null=True, blank=True,
    )
    owner = models.ForeignKey(User, related_name='fixed_costs', on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField(CostTag, related_name='fixed_costs')


class VariableCost(models.Model):
    name = models.CharField(max_length=400, unique=False)
    amount = models.IntegerField()
    date = models.DateTimeField()

    context = models.ForeignKey(
        Context, on_delete=models.CASCADE, related_name='variable_costs',
        default=None, null=True, blank=True,
    )
    owner = models.ForeignKey(User, related_name='variable_costs', on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField(CostTag, related_name='variable_costs')
