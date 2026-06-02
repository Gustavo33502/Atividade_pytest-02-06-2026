import pytest
import smtplib
from src.notificacoes.servico import enviar_email, enviar_boas_vindas

@pytest.fixture
def setup_env(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "remetente@test.com")
    monkeypatch.setenv("SMTP_PASS", "senha_segura")

def test_enviar_email_sucesso(mocker, setup_env):
    mock_smtp = mocker.patch("src.notificacoes.servico.smtplib.SMTP") 
    mock_inst = mock_smtp.return_value.__enter__.return_value 

    resultado = enviar_email("dest@test.com", "assunto", "corpo")   

    assert resultado is True
    mock_smtp.assert_called_once_with("smtp.test.com", 587) 
    mock_inst.starttls.assert_called_once() 
    mock_inst.login.assert_called_once_with("remetente@test.com", "senha_segura") 

def test_sem_credenciais_levanta_erro(monkeypatch):
    monkeypatch.delenv("SMTP_USER", raising=False) 
    monkeypatch.delenv("SMTP_PASS", raising=False)

    with pytest.raises(EnvironmentError, match="obrigatórios"): 
        enviar_email("dest@test.com", "assunto", "corpo")


def test_enviar_email_falha_apos_3_tentativas(mocker, setup_env):
  
    mocker.patch("src.notificacoes.servico.smtplib.SMTP", side_effect=smtplib.SMTPException("Erro de conexão"))
    

    mock_time = mocker.patch("src.notificacoes.servico.time")

    
    resultado = enviar_email("dest@test.com", "assunto", "corpo")

  
    assert resultado is False
    
  
    assert mock_time.sleep.call_count == 2

def test_enviar_boas_vindas(mocker, setup_env):
    mock_enviar = mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)

    resultado = enviar_boas_vindas(email="novo@test.com", nome="Elizabeth") 

    assert resultado is True
    mock_enviar.assert_called_once_with(
        destinatario="novo@test.com",
        assunto="Bem-vindo ao nosso serviço!",
        corpo=mocker.ANY 
    )