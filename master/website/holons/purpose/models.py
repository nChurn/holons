from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import User
from moneta.models import BusinessEntity

@receiver(post_save, sender=BusinessEntity)
def new_entity_makes_context(instance, created, **kwargs):
    if not created:
        return

    Context(entity=instance).save()
    
class Context(models.Model):
    user_personal = models.OneToOneField(User, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="personal_purpose_context",
    )
    user_handle = models.OneToOneField(User, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="handle_purpose_context",
    )
    entity = models.OneToOneField(BusinessEntity, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name="purpose_context",
    )

    @property
    def type(self):
        for f in Context._meta.fields:
            f_value = getattr(self, f.name)
            if(f_value != None and f.name != 'id'):
                return f.name
    
    @property
    def foreign(self):
        aliases = {
            'user_personal': lambda instance: 'personal',
            'user_handle': lambda instance: instance.handle,
            'entity': lambda instance: instance.name
        }

        for f in Context._meta.fields:
            f_value = getattr(self, f.name)
            if(f_value != None and f.name != 'id'):
                return {'id': str(f_value.id), 'name': aliases[f.name](f_value)}
    
    @property
    def owner(self):
        if self.type == 'entity':
            return self.entity.owner.first()
        else:
            return self.user_handle or self.user_personal

def now_plus_half_year():
    return timezone.now() + timezone.timedelta(days=365/2)

class Purpose(models.Model):
    title = models.CharField(max_length=255, blank=True)
    start_at = models.DateTimeField(blank=True, null=True) # if this field is not Null season is launched
    finish_at = models.DateTimeField(blank=True, null=True) # if this field is not Null season is finished
    plan_end_date = models.DateTimeField(default=now_plus_half_year)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="purposes")
    context = models.ForeignKey(Context, on_delete=models.CASCADE, null=True, blank=True, related_name="purposes")

    @property
    def status(self):
        status = 'draft'
        for f in Purpose._meta.fields:
            f_value = getattr(self, f.name)
            if(f_value != None and '_at' in f.name):
                status =  f.name.replace('_at', '')
        return status
        


class Objective(models.Model):
    title = models.CharField(max_length=255)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, related_name="objectives")

    @property
    def is_done(self):
        for kr in KeyResult.objects.filter(objective_id=self.id):
            if not kr.done_at:
                return False

        return True
    
    @property
    def owner(self):
        return self.purpose.owner

class KeyResultType(models.Model):
    name = models.CharField(max_length=255)
    
class KeyResult(models.Model):
    title = models.CharField(max_length=255)
    done_at = models.DateTimeField(blank=True, null=True) # if this field is not Null key result is done
    current_value = models.FloatField(default=0, blank=True)
    target_value = models.FloatField(default=1, blank=True)
    interval = models.IntegerField(default=1, null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_krs')
    type = models.ForeignKey(KeyResultType, on_delete=models.PROTECT)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE, related_name="key_results")
    
    @property
    def creator(self):
        return self.objective.purpose.owner
    @property
    def context(self):
        return self.objective.purpose.context
    @property
    def purpose(self):
        return self.objective.purpose

    @property
    def next_check_in(self):
        next_sunday = (timezone.now() + timezone.timedelta(7 - (timezone.now().weekday() + 1)))
        return CheckIn.objects.filter(key_result_id=self.id, date__year=next_sunday.year, date__month=next_sunday.month, date__day=next_sunday.day).first()

@receiver(pre_save, sender=KeyResult)
def check_if_kr_is_done(instance, **kwargs):
    if round(instance.current_value, 2) == round(instance.target_value, 2):
        instance.done_at = timezone.now()


class CheckIn(models.Model):
    date = models.DateTimeField()
    fact = models.TextField(default='')
    plan = models.TextField(default='')
    current_value = models.FloatField(default=0)

    key_result = models.ForeignKey(KeyResult, on_delete=models.CASCADE, related_name="check_ins")
