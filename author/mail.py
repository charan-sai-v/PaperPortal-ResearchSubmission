from django.core.mail import send_mail
from django.conf import settings


# send confirmation mail to user
def send_confirmation_mail(user, token):
    subject = 'Confirm your account'
    name = user['name']
    message = f'Hi {name},\n\nPlease confirm your account by clicking on the link below:\n\nhttp://localhost:8000/author/confirmation/{token}\n\nThanks,\nTeam Rescone'
    email_from = settings.EMAIL_HOST_USER
    mail = user['email']
    recipient_list = [mail]
    send_mail(subject, message, email_from, recipient_list)


# send password reset mail to user
def send_password_reset_mail(user, token):
    subject = 'Reset your password'
    name = user['name']
    message = f'Hi {name},\n\nPlease reset your password by clicking on the link below:\n\nhttp://localhost:8000/author/reset_password/{token}\n\nThanks,\nTeam Rescone'
    email_from = settings.EMAIL_HOST_USER
    mail = user['email']
    recipient_list = [mail]
    send_mail(subject, message, email_from, recipient_list)