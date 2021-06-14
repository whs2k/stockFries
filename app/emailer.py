# Built-in
import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Tuple
# Internal
from config import SMTP_PORT, SMTP_SERVER, SENDER_EMAIL, EMAIL_PASSWORD, RECEIVER_EMAIL_ERROR



class EmailBase:
    """Base class for email that prepares SMTP, defaulting to values provided in config.py. Used as a standalone for
    internal use such as error email sending. Otherwise used in the EmailMain class where the only arg that will be
    overwritten is the receiver_email."""

    def __init__(
            self,
            smtp_port: int = SMTP_PORT,
            smtp_server: str = SMTP_SERVER,
            sender_email: str = SENDER_EMAIL,
            email_password: str = EMAIL_PASSWORD,
            receiver_email: str = SENDER_EMAIL,
            receiver_email_error: str = RECEIVER_EMAIL_ERROR):

        self.smtp_port = smtp_port
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.email_password = email_password
        self.receiver_email = receiver_email
        self.receiver_email_error = receiver_email_error

    def email_send(self, subject: str, text: str, completion: str,
                   error_ping: bool = False) -> None:

        if error_ping:
            RECEIVE_EMAIL = self.receiver_email_error
        else:
            RECEIVE_EMAIL = self.receiver_email

        # Sends with CC to dev
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVE_EMAIL

        part1 = MIMEText(text, "plain")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
        context.minimum_version = ssl.TLSVersion["TLSv1_1"]
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.set_debuglevel(1)
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, [RECEIVE_EMAIL, RECEIVER_EMAIL_ERROR], message.as_string())
        print(completion)

    def email_template(self, fn: str) -> None:

        subject = text = completion = 'Function {}'.format(fn)
        self.email_send(subject, text, completion, error_ping=True)

