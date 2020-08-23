import datetime as dt
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
from blog import models
from threading import Thread

app = Flask(__name__)
app.secret_key = "Vegeta#5"
app_root = os.path.dirname(os.path.abspath(__file__))

def send_async_email(app, msg):

    with app.app_context():
        users = models.get_subscribe_users()
        email_user = 'mountainblaster00@gmail.com'
        email_receiver = []
        for row in users:
            email_receiver.append(row.email)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, 'Vegeta#5')
        server.sendmail(email_user, email_receiver, msg.as_string())
        server.quit()


def send_email():
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Newsletter Neo4j"
    msg['From'] = None
    msg['To'] = None

    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
            <html>
              <head></head>
              <body>
                <p>Hello!<br>
                   How are you?<br>
                   Il y a de nouvelles publications qui pourraient t'intéresser". Cliquez sur le sur ci-dessous pour y être rediriger<br>
                   <a href="http://127.0.0.1:5000/">lien du site</a>.<br>
                   Merci de vous être souscrit. :)
                </p>
              </body>
            </html>"""

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


first_email_time = dt.datetime.now()  # set your sending time in UTC
interval = dt.timedelta(minutes=1)  # set the interval for sending the email
send_time = first_email_time + interval


while True:
    if send_time < dt.datetime.now():
        send_email()
        print('email sent')
        send_time = send_time + interval

