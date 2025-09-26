import smtplib
from email.message import EmailMessage

from config import Config
from file_manager import FileManager

class EmailManager:
  def __init__(self):
      self.file_manager = FileManager()
      self.config = Config()

  # E-mail To, From, Subject, Body
  def send_email(self, content, content_title="Here are the available appointments at your GP practice:", title="🩺 Available GP Appointments"):
      try:
          email_msg = EmailMessage()
          email_msg["To"] = self.config.EMAIL_TO
          email_msg["From"] = self.config.EMAIL_FROM       
          email_msg["Subject"] = title

          email_msg.set_content(content)
          email_msg.add_alternative(f"""
          <html>
            <body>
              <p>{content_title}</p>
              {content}
            </body>
          </html>
          """, subtype='html')

          with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
              server.login(self.config.EMAIL_FROM, self.config.EMAIL_PASSWORD)
              server.send_message(email_msg)

      except Exception as e:
          self.file_manager.log_error(f"Failed to send email: {e}")
