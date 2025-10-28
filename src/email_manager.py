import smtplib
from email.message import EmailMessage

from config import Config

class EmailManager:
  def __init__(self):
      self.config = Config()

  def send_email(self, content, email_content_title, title="🩺 Available GP Appointments"):
    # Clean text to prevent newlines in headers
    clean_title = title.replace("\r", " ").replace("\n", " ").strip()
    clean_content_title = email_content_title.replace("\r", " ").replace("\n", " ").strip()

    # HTML clean body - user view
    html_body = f"""
    <html>
      <body>
        <p>{clean_content_title}</p>
        {content}
      </body>
    </html>
    """
    
    try:
        email_msg = EmailMessage()
        email_msg["To"] = self.config.EMAIL_TO
        email_msg["From"] = self.config.EMAIL_FROM       
        email_msg["Subject"] = clean_title

        # Plaintext fallback - if the recipient’s email client can’t or won’t render HTML
        email_msg.set_content(f"{clean_content_title}\n\n{content}")

        # HTML version
        email_msg.add_alternative(html_body, subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.config.EMAIL_FROM, self.config.EMAIL_PASSWORD)
            server.send_message(email_msg)

    except Exception as e:
      print(f"Failed to send email: : {e}")
