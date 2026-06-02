import json
import pytest
from src.notificacoes.gerenciador import GerenciadorDeNotificacoes

def test_notificar_usuario_retorna_dict_com_campos_corretos(mocker):
    mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("src.notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    registro = gerenciador.notificar_usuario(nome="Elizabeth", email="elizabeth@exemplo.com", telefone="+123456789")
    
    assert isinstance(registro, dict)
    assert registro["email_enviado"] is True

def test_notificar_usuario_chama_email_e_sms(mocker):
    mock_email = mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)
    mock_sms = mocker.patch("src.notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    gerenciador.notificar_usuario(nome="Maria", email="maria@exemplo.com", telefone="+987654321")
    
    mock_email.assert_called_once()
    mock_sms.assert_called_once()

def test_historico_e_atualizado_apos_notificacao(mocker):
    mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("src.notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    assert len(gerenciador.historico) == 0
    
    gerenciador.notificar_usuario(nome="Gustavo", email="gustavo@exemplo.com", telefone="+111222333")
    assert len(gerenciador.historico) == 1

def test_resumo_conta_envios_corretamente(mocker):
    mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("src.notificacoes.sms.enviar_codigo_verificacao", return_value=True)
    
    gerenciador = GerenciadorDeNotificacoes()
    gerenciador.notificar_usuario("User1", "user1@teste.com", "+111")
    gerenciador.notificar_usuario("User2", "user2@teste.com", "+222")
    
    dados_resumo = gerenciador.resumo()
    assert dados_resumo["total"] == 2


def test_reenviar_falhas_atualiza_historico_com_sucesso(mocker):
    
    mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("src.notificacoes.sms.enviar_codigo_verificacao", return_value=True)

    gerenciador = GerenciadorDeNotificacoes()

    gerenciador.historico.append({
        "nome": "Felipe", "email": "felipe@test.com", "telefone": "999",
        "email_enviado": False, "sms_enviado": False
    })

    reenvios = gerenciador.reenviar_falhas()
    
    assert reenvios == 1
    assert gerenciador.historico[0]["email_enviado"] is True
    assert gerenciador.historico[0]["sms_enviado"] is True

def test_exportar_historico_salva_arquivo_correto(mocker, tmp_path):
    
    mocker.patch("src.notificacoes.servico.enviar_email", return_value=True)
    mocker.patch("src.notificacoes.sms.enviar_codigo_verificacao", return_value=True)

    gerenciador = GerenciadorDeNotificacoes()
    gerenciador.notificar_usuario(nome="Alice", email="alice@test.com", telefone="111")

    arquivo_destino = tmp_path / "historico.json"
    caminho_str = str(arquivo_destino)

    gerenciador.exportar_historico(caminho_str)

    assert arquivo_destino.exists() is True
    with open(caminho_str, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    assert dados[0]["nome"] == "Alice"