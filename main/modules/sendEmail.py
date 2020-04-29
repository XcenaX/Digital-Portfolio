import smtplib

from django.core.mail import send_mail
from django.conf import settings

# def send_email(content, email_to):
#     server = smtplib.SMTP("smtp.gmail.com:587")
#     server.ehlo()
#     server.starttls()
#     server.login(EMAIL, PASSWORD)
#     message = "Subject: {}\n\n{}".format("Nova support", content)
#     server.sendmail(EMAIL, email_to, message)
#     server.quit()

def send_email(content, subject, email_to):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_to]
    send_mail( subject, content, email_from, recipient_list )