import threading

from .models import Users
from .token import account_activation_token
from my_settings import EMAIL

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)


def send_email(request, user_id, *args, **kwargs):
    user = Users.objects.get(pk=user_id)
    subject = '{}님의 회원가입 인증메일입니다.'.format(user.nickname)
    body = ''
    from_email = EMAIL['EMAIL_HOST_USER']
    recipient_list = [user.email]
    fail_silently = False
    html = render_to_string('accounts/activation_mail.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
        'domain': request.META['HTTP_HOST'],
        'token': account_activation_token.make_token(user)
    })
    EmailThread(subject, body, from_email, recipient_list,
                fail_silently, html).start()
    print(request.META['HTTP_HOST'])


def get_uid(uid64):
    uid = force_text(urlsafe_base64_decode(uid64))
    return uid
