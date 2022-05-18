import logging
from io import StringIO
from html.parser import HTMLParser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

SENDGRID_API_KEY = settings.SENDGRID_API_KEY
SENDGRID_DOMAINS_API_KEY = settings.SENDGRID_DOMAINS_API_KEY
SENDGRID_DOMAINS_SUBUSER = settings.SENDGRID_DOMAINS_SUBUSER
SENDGRID_DOMAINS_IP = settings.SENDGRID_DOMAINS_IP


def send_email(mail_from: str = '', mail_to: str = '', subject: str = '', body: str = '', body_plain: str = '') -> bool:
    """
    Mother of all — core email-sending function
    Basically self-explanatory

    :param mail_from:
    :param mail_to:
    :param subject:
    :param body:
    :return:
    """

    if not body_plain:
      body_plain = strip_tags(body)

    if mail_from == '' or mail_to == '':
        return False

    message = Mail(
        from_email=mail_from,
        to_emails=mail_to,
        subject=subject,
        html_content=body,
        plain_text_content=body_plain
        )
    try:
        sg = SendGridAPIClient(SENDGRID_DOMAINS_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e.message)
    logging.info('Send email from: ' + str(mail_from) + ' to:'  + str(mail_to) + ' subject:' + subject)
    return True


class MLStripper(HTMLParser):
    """
    This is cut and paste from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
