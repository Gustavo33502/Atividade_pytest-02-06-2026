import pytest
from src.notificacoes.sms import enviar_sms, enviar_codigo_verificacao

def test_enviar_sms_sucesso(monkeypatch):
    monkeypatch.setenv("SMS_REMETENTE", "+1234567890") 
    destinatario = "+0987654321"
    mensagem = "Bem-vindo ao nosso serviço!"
    resultado = enviar_sms(destinatario=destinatario, mensagem=mensagem)
    assert resultado is True

def test_sem_remetente_levanta_erro(monkeypatch):
    monkeypatch.delenv("SMS_REMETENTE", raising=False)
    destinatario = "+0987654321"
    mensagem = "Bem-vindo!"
    with pytest.raises(EnvironmentError) as exc_info:
        enviar_sms(destinatario=destinatario, mensagem=mensagem)
    assert "SMS_REMETENTE' é obrigatória" in str(exc_info.value)

def test_enviar_codigo_verificacao(mocker):
    mock_enviar_sms = mocker.patch('src.notificacoes.sms.enviar_sms', return_value=True)
    telefone = "+0987654321"
    codigo = "123456"
    
    enviar_codigo_verificacao(telefone=telefone, codigo=codigo)
    
    mock_enviar_sms.assert_called_once_with(
        destinatario=telefone, 
        mensagem="Seu código de verificação é: 123456"
    )