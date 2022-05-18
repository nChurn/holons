from django.db import models
from django_mailbox.models import Message as DjangoMailboxMessage


class Mailbox(models.Model):
    """
    Meta-data about mailbox
    Real mailbox is taken care of DjangoMailbox, which connects to real mail server via IMAP
    """

    name = models.CharField(max_length=255)
    incoming_email = models.CharField(max_length=255, default='')
    domain = models.CharField(max_length=255, default='')
    domain_id = models.IntegerField(default=0)
    domain_ip = models.CharField(max_length=255, default='')
    sendgrid_subuser = models.CharField(max_length=255, default='')
    dns_mail_cname = models.CharField(max_length=255, default='')
    dns_mail_cname_data = models.CharField(max_length=255, default='')
    dns_dkim1 = models.CharField(max_length=255, default='')
    dns_dkim1_data = models.CharField(max_length=255, default='')
    dns_dkim2 = models.CharField(max_length=255, default='')
    dns_dkim2_data = models.CharField(max_length=255, default='')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    is_frontapp_import = models.BooleanField(default=False)
    frontapp_token = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class SharedMailMessage(models.Model):
    """
    Pivot model for sharing messages between users
    """

    assigned_to_id = models.IntegerField(default=None)
    assigned_by_id = models.IntegerField(default=None)
    mailbox_from_id = models.IntegerField(default=None)
    mailbox_to_id = models.IntegerField(default=None)
    messages = models.ManyToManyField(DjangoMailboxMessage, blank=True)

    def __str__(self):
        return 'from: ' + str(self.mailbox_from_id) + ' to: ' + str(self.mailbox_to_id) 

    def __unicode__(self):
        return 'from: ' + str(self.mailbox_from_id) + ' to: ' + str(self.mailbox_to_id) 


class EmailConversations(models.Model):
    """
    Connect separate email messages into conversations
    """

    conversation_id = models.CharField(max_length=255)
    subject = models.CharField(max_length=1024, default='')
    status = models.CharField(max_length=255)
    messages = models.ManyToManyField(DjangoMailboxMessage, related_name='conversation', blank=True)

    def __str__(self):
        return self.conversation_id

    def __unicode__(self):
        return self.conversation_id


class MailMessageStatus(models.Model):
    """
    Status records for separate emails
    """

    message_id = models.IntegerField(default=0, unique=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_snoozed = models.BooleanField(default=False)
    snoozed_until = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class EmailImportStatus(models.Model):
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE, default=False)
    status = models.CharField(max_length=255, default='')
    conversation_count = models.IntegerField(default=0)
    message_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True)
    completed_at = models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True)

    def __str__(self):
        return self.mailbox.name

    def __unicode__(self):
        return self.mailbox.name

