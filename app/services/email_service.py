import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(to_email, subject, message):
    try:
        # Criar mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = settings.from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Enviar e-mail usando o servidor SMTP
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.from_email, to_email, msg.as_string())

    except Exception as e:
        raise Exception(f"Erro ao enviar e-mail: {e}")
