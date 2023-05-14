from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import send_mail
import requests
import json

class Email_Backend(BaseEmailBackend):
  def send_messages(email_messages):
    num = 0
    for email in email_messages:
      num = num + 1
      res = requests.post(
          "https://api.mailgun.net/v3/testmp.stix.site/messages",
          auth=("api", "f2a36cb54ee3e4953af6c97b38dd6cab-915161b7-6458b7be"),
          params={"address": email.from_email},
          data={
            "subject": "My subject",
            "from": email.from_email,
            "to": email.to,
            "text": "The text",
            "html": "testing"
          })
    return num
    
  def open(self):
    return
  
  def close(self):
    return
  
  
def sendtest():
  return send_mail('subjectyoyoyoyo', 'body of the message', 'wenxuan27@outlook.com', ['wenxuan27@live.cn'])