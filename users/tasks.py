from celery import shared_task


@shared_task(bind=True)
def send_welcome_mail_to_department_admin(self):
    print("send_welcome_mail_to_department_admin")


@shared_task(bind=True)
def send_mail_on_department_create(self):
    print("send_mail_on_department_create")
