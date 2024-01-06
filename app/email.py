import configparser
import pandas as pd
import smtplib
from .database import TefasDatabase
from .logconfig import setup_logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders




def send_email(file_to_send):

    logger = setup_logger(__name__)

    logger.info("Starting email process...")

    database = TefasDatabase()
    df_profit = database.read_table("tbl_tefas_profit")

    logger.info(f"Exporting {file_to_send} to excel spreadsheet...")
    df_profit.to_excel("export/" + file_to_send, index=False)
    logger.info(f"Exported {file_to_send} to excel spreadsheet...")


    logger.info("Reading email settings from properties file")

    config = configparser.ConfigParser()
    config.read('config/email_config.properties')
    # Debug: Print all sections to see what is being read
    logger.info(f"Sections found: {config.sections()}")

    email_user = config['EmailSettings']['email_user']
    email_password = config['EmailSettings']['email_password']
    email_send = config['EmailSettings']['email_send'].split(', ')

    logger.info(f"Email is being sent to {email_send} from {email_user}")

    subject = 'Tefas Profit Export'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ', '.join(email_send)
    msg['Subject'] = subject

    body = 'Here is the Tefas table export.'
    msg.attach(MIMEText(body, 'plain'))

    logger.info("File is being attached")
    attachment = open("export/" + file_to_send, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename="+file_to_send)

    msg.attach(part)
    text = msg.as_string()

    # GMX Mail SMTP settings
    server = smtplib.SMTP('mail.gmx.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    logger.info("Email is being sent...")
    server.sendmail(email_user, email_send, text)
    logger.info("Email sent!")
    server.quit()
