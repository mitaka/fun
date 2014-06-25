from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def send_html_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    text_part = strip_tags(message)
    msg = EmailMultiAlternatives(subject, text_part, from_email, recipient_list)
    msg.attach_alternative(message, "text/html")
    return msg.send()
