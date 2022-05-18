from django.db import models


class Log(models.Model):
    event_type = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    is_sent = models.BooleanField(default=False)
    check_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_type + ' ' + str(self.check_date)

    def __unicode__(self):
        return self.event_type + ' ' + str(self.check_date)


class TalentStat(models.Model):
    messages_master = models.IntegerField(default=0)
    messages_rays = models.IntegerField(default=0)
    check_date = models.DateTimeField(auto_now=False)

    def __str__(self):
        return str(self.messages_master) + ' : '  + str(self.messages_rays) + ' ' + str(self.check_date)

    def __unicode__(self):
        return str(self.messages_master) + ' : '  + str(self.messages_rays) + ' ' + str(self.check_date)


