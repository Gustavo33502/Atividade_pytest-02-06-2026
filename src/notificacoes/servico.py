import logging
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.notificacoes import templates

logger = logging.getLogger(__name__)

def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    usuario = os.getenv("SMTP_USER")
    senha = os.getenv("SMTP_PASS")

    if not usuario or not senha: 
        raise EnvironmentError("SMTP_USER e SMTP_PASS são obrigatórios")
    
    msg = MIMEMultipart()
    msg['subject'] = assunto
    msg['From'] = usuario
    msg['To'] = destinatario
    msg.attach(MIMEText(corpo, "plain"))

    tentativas_maximas = 3
    
    for tentativa in range(1, tentativas_maximas + 1):
        try:
            logger.info(f"Tentativa {tentativa} de enviar e-mail para {destinatario}...")
            
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(usuario, senha)
                server.send_message(msg)
            
            logger.info(f"Email enviado com sucesso para {destinatario} na tentativa {tentativa}!")
            return True
            
        except Exception as erro:
            logger.warning(f"Falha na tentativa {tentativa}: {erro}")
   
            if tentativa < tentativas_maximas:
                time.sleep(1)

    logger.error(f"Não foi possível enviar o e-mail após {tentativas_maximas} tentativas.")
    return False

def enviar_boas_vindas(email: str, nome: str) -> bool:
    dados_email = templates.boas_vindas(nome) 
    return enviar_email(
        destinatario=email, 
        assunto=dados_email['assunto'], 
        corpo=dados_email['corpo']
        )
