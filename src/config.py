import os
from dotenv import load_dotenv

load_dotenv(override=True)  # loads variables from .env file

class Config:
  
  USERNAME = os.getenv('USERNAME')
  PASSWORD = os.getenv('PASSWORD')

  EMAIL_FROM = os.getenv('EMAIL_FROM')
  EMAIL_TO = os.getenv('EMAIL_TO')
  EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

  EMAIL_SUBJECT = '🩺 New GP Appointment Available!'

  APPT_FILE = '/tmp/available_appointments.txt'
  LOG_FILE = '/tmp/systm_log.err'
  
  @classmethod
  def validate(cls):
      missing = []
      for attr in ['USERNAME', 'PASSWORD', 'EMAIL_FROM', 'EMAIL_TO', 'EMAIL_PASSWORD']:
          if not getattr(cls, attr):
              missing.append(attr)
      if missing:
          raise ValueError(f"Missing required environment variables: {', '.join(missing)}")