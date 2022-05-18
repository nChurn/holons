from django.db import models
from accounts.models import User

class PaysendAccount(models.Model):
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE,  
        related_name="paysend_account",
    )
    card_number = models.CharField(max_length=50, null=True, blank=True)
    # addon information here

class StripeAccount(models.Model):
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE,  
        related_name="stripe_account",
    )
    # addon information here