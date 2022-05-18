from django.db import models


class Talent(models.Model):
    profile_url = models.CharField(max_length=8192, default=None, null=True)
    name = models.CharField(max_length=8192, default=None, null=True)
    first_name = models.CharField(max_length=8192, default=None, null=True)
    last_name = models.CharField(max_length=8192, default=None, null=True)
    company_name = models.CharField(max_length=8192, default=None, null=True)
    title = models.CharField(max_length=8192, default=None, null=True)
    company_id = models.CharField(max_length=8192, default=None, null=True)
    company_url = models.CharField(max_length=8192, default=None, null=True)
    summary = models.TextField(default=None, null=True)
    location = models.CharField(max_length=256, default=None, null=True)
    duration = models.CharField(max_length=256, default=None, null=True)
    past_role = models.CharField(max_length=256, default=None, null=True)
    past_company = models.CharField(max_length=256, default=None, null=True)
    past_company_url = models.CharField(max_length=256, default=None, null=True)
    profile_image_url = models.CharField(max_length=8192, default=None, null=True)
    shared_connections_count = models.CharField(
      max_length=8192, default=None, null=True
    )
    vmid = models.CharField(max_length=8192, default=None, null=True)
    is_premium = models.BooleanField(default=False)
    query = models.CharField(max_length=8192, default=None, null=True)
    timestamp = models.CharField(max_length=8192, default=None, null=True)
    source = models.CharField(max_length=256, default=None, null=True)
    total_jobs = models.IntegerField(default=None, null=True)
    completed_jobs = models.IntegerField(default=None, null=True)
    total_earnings = models.IntegerField(default=None, null=True)
    total_hours = models.IntegerField(default=None, null=True)
    hourly_rate = models.IntegerField(default=None, null=True)

    class Meta:
        app_label = 'rays'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

