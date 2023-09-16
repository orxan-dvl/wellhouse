from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import BlogPage, SubscriberForm

@receiver(post_save, sender=BlogPage)
def send_blog_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Blog Published: {}'.format(instance.title)
        message = 'Check out our latest blog: {}'.format(instance.url)
        from_email = 'zekiyev014@gmail.com'  # Replace with your email
        recipient_list = [subscriber.email for subscriber in SubscriberForm.objects.all()]
        send_mail(subject, message, from_email, recipient_list)
