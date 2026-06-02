# teste de integração
import os
import pytest
from src.notificacoes.servico import enviar_boas_vindas, enviar_email

@pytest.fixture(autouse=True)
def verificar_credenciais():
    if not os.getenv("SMTP_USER") or not os.getenv("SMTP_PASS"):
        pytest.skip("Credenciais SMTP não configuradas (SMTP_USER / SMTP_PASS)")
    
def test_enviar_email_real():
    destinatario = os.getenv("EMAIL_DESTINO", os.getenv("SMTP_USER"))  
    
    resultado = enviar_email(
        destinatario=destinatario,
        assunto="[Teste de Integração]",
        corpo="Este é um teste de integração para o serviço de notificações. \n \n funcionou! 🎉"
    )

    assert resultado is True

def test_enviar_boas_vindas_real():
    destinatario = os.getenv("EMAIL_DESTINO", os.getenv("SMTP_USER"))  
    
    resultado = enviar_boas_vindas(email=destinatario, nome="aluno")

    assert resultado is True