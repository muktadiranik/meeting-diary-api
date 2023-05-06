from django.db.models.signals import post_save
from django.dispatch import receiver
from meetings.models import Meeting
from meetings.tasks import send_invitation_mail_to_invited_members


@receiver(post_save, sender=Meeting)
def send_invitation_mail(sender, **kwargs):
    print(kwargs)
    if kwargs["instance"]:
        email_list = ""
        for i in kwargs["instance"].invited_member.all():
            email_list += i.email + " "
        send_invitation_mail_to_invited_members.delay(
            email_list, kwargs["instance"].id
        )
