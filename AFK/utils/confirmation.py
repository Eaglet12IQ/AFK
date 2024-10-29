import random
import threading
from django.conf import settings
from django.core.mail import send_mail

def send_confirmation_email(email, confirmation_code):
    subject = 'Email Confirmation'
    message = f'Your confirmation code is: {confirmation_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    threading.Thread(target=send_mail, args=(subject, message, email_from, recipient_list)).start()

def generate_numeric_code(length=6):
    return str(random.randint(10**(length-1), 10**length - 1))