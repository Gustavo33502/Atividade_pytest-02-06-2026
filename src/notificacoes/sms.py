import logging
import os

logger = logging.getLogger(__name__) 

def enviar_sms(destinatario: str, mensagem: str) -> bool: 

    remetente = os.getenv('SMS_REMETENTE') 

    if not remetente: 
        raise EnvironmentError("A variável de ambiente 'SMS_REMETENTE' é obrigatória.") 
    
    print(f"[SMS] De: {remetente} | Para: {destinatario} | Mensagem: {mensagem}")

    logger.info(f"SMS enviado para {destinatario}")

    return True

def enviar_codigo_verificacao(telefone: str, codigo: str) -> bool: 

    mensagem = f"Seu código de verificação é: {codigo}" 

    return enviar_sms(destinatario=telefone, mensagem=mensagem) 