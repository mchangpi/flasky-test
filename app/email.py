import os
from threading import Thread
from flask import current_app, render_template
# from flask_mail import Message
# from . import mail

import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail


def send_async_email(app, msg):
    with app.app_context():
        # mail.send(msg)
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        response = sg.client.mail.send.post(request_body=msg.get())
        print('response ', response)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    """
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    """
    from_email = Email(app.config['FLASKY_MAIL_SENDER'])
    to_email = To(to)
    subject = "Sending with SendGrid is Fun"
    plain_content = Content("text/plain", render_template(template + '.txt', **kwargs))
    html_content = Content("text/html", render_template(template + '.html', **kwargs))
    msg = Mail(from_email, to_email, subject, html_content)
    msg.add_content(plain_content)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr