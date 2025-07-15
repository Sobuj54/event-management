from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        recipients = [instance.email]
        subject = "Activate your account."
        message = f"""
                        Hello,

                        You need to activate your account.
                        Follow the url:
                        {activation_url}

                        Please log in to your dashboard to manage it.

                        Regards,
                        Task Management System
                    """
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False
            )
            print(f"[signal] Mail sent successfully.")
        except Exception as e:
            print(f"Failed to send email to {instance.email}\n error: {str(e)}")