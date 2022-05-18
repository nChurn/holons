from django.db import models
from moneta.models import BusinessEntity
from relations.models import Offer


class WorkPeriod(models.Model):
    """Timer (when it was started and stopped)
    """

    user_id = models.IntegerField(null=True)
    timer_start = models.DateTimeField(null=True)
    timer_stop = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)
    commitment = models.ForeignKey(Offer,
                                        blank=True,
                                        on_delete=models.CASCADE,
                                        null=True)
    business_entity = models.ForeignKey(BusinessEntity,
                                        blank=True,
                                        on_delete=models.CASCADE,
                                        default=False)
    comment = models.TextField(blank=True, default='')
    is_billable = models.BooleanField(default=True)


    @property
    def business_entity_title(self):
        return str(self.business_entity)
    @property
    def commitment_title(self):
        return str(self.commitment)

    class Meta:
        app_label = 'timer'

    def __str__(self):
        return str(self.duration)



"""
1.1. Query (get) request with this user_id and no time_stop (if true - time_stop and duration, else (first step))
1. Post request: user_id
2. Add times_temp to model and save (without time stop)
3. Post request: user_id
"""

"""
1. Request GET time_periods: take all sum of hours (request to dB)
2. Select user_id, sum (duration) from work_periods group by user_id
"""


class UserInfo(models.Model):
    """Users and their work"""

    user_id = models.IntegerField(null=True)
    worked_hours = models.IntegerField(null=True)
    paid_hours = models.IntegerField(null=True)
    rate = models.FloatField(null=True)

    class Meta:
        app_label = 'timer'

    def __str__(self):
        return str(self.rate)



