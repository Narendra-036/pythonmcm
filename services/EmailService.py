import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailService:
    @staticmethod
    def send_email(recipients, subject, html_content):
        """
        Send an email to the specified recipients.

        Args:
            recipients (list): List of email addresses to send to.
            subject (str): Email subject line.
            html_content (str): HTML content of the email.

        Raises:
            Exception: If email sending fails.
        """
        # Email configuration from environment variables
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_email = os.getenv('FROM_EMAIL', smtp_user)

        if not smtp_user or not smtp_password:
            logging.error("SMTP credentials not configured")
            raise ValueError("SMTP credentials not configured")

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = ', '.join(recipients)

        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)

        try:
            # Connect to SMTP server
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(message)
                
            logging.info(f"Email sent successfully to {', '.join(recipients)}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            raise
