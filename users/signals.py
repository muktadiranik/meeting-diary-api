from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from users.tasks import *
from meetings.models import Department
User = get_user_model()


@receiver(post_save, sender=User)
def send_mail_on_user_post_save(sender, instance, created, **kwargs):
    send_welcome_mail_to_department_admin.delay()


@receiver(post_save, sender=Department)
def send_mail_on_department_post_save(sender, instance, created, **kwargs):
    send_mail_on_department_create.delay()
