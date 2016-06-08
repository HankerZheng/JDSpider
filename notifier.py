#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class SendEMail(object):
    """
    This is the notifier module.
    Given an input dictionary containing data with item_name and price,
    warp them into an e-mail and send it to the specific receiver.
    """
    def __init__(self, content, config, subject):
        self.to_addr = config["to_addr"]
        self.from_addr = config["from_addr"]
        self.password = config["password"]

        self.host = config["host"]
        self.port = config["port"]

        self.subject = subject
        self.content = content

        self.timeout = config["timeout"]

    def __call__(self):
        msg = MIMEText(self.content, "plain", "utf-8")
        msg['From'] = 'JDSpider <%s>' % self.from_addr
        msg['To'] = 'Receiver <%s>' % self.to_addr
        msg['Subject'] = Header(self.subject,'utf-8')

        try:
            server = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            server.set_debuglevel(1)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, self.to_addr, msg.as_string())
            server.quit()
        except smtplib.SMTPException, e:
            raise ValueError(e)

