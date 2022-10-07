import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.utils.logger_utils import get_logger
from config import NotifierConfig

logger = get_logger("Email Service")


class EmailService:
    def __init__(self, email_address=NotifierConfig.MAIL_ADDRESS, email_password=NotifierConfig.MAIL_PASSWORD):
        self.address = email_address
        self.password = email_password

        self.server = None

    # def reconnect(self):
    #     # Set up the server
    #     context = ssl.create_default_context()
    #     self.server = smtplib.SMTP_SSL(NotifierConfig.MAIL_HOST, NotifierConfig.MAIL_PORT, context=context)
    #
    #     # Authentication
    #     self.server.login(self.address, self.password)

    # def get_subscribers(self):
    #     subscribes_info = self.db.get_config(MongoKeys.email_subscribes)
    #     return subscribes_info.get('addresses', {}) if subscribes_info else {}
    #
    # def subscribe(self, address, email):
    #     subscribers = self.get_subscribers()
    #     subscribers[address] = email
    #     self.db.set_config(MongoKeys.email_subscribes, {'addresses': subscribers})
    #
    # def unsubscribe(self, address):
    #     subscribers = self.get_subscribers()
    #     if address in subscribers:
    #         subscribers.pop(address)
    #         self.db.set_config(MongoKeys.email_subscribes, {'addresses': subscribers})

    def send(self, recipients, subject, html):
        """
        Send test mail to one or a list of recipients
        Does not work for mail aliases 
        """
        # Set up the msg object
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject 
        msg['From'] = f'BRicher <{self.address}>'
        msg['To'] = ",".join(recipients) if isinstance(recipients, list) else recipients

        # Create content for the message
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        # Send
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(NotifierConfig.MAIL_HOST, NotifierConfig.MAIL_PORT, context=context) as server:
                server.login(self.address, self.password)
                server.sendmail(msg['From'], recipients, msg.as_string())

            logger.info(f"Send mail to {recipients}")
            return msg
        except Exception as ex:
            logger.exception(ex)
