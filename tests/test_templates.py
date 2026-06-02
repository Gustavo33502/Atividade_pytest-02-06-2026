import pytest
from src.notificacoes.templates import boas_vindas, recuperacao_senha, confirmacao_pedido

def test_boas_vindas_retorna_assunto_corpo():
    nome_usuario = "Gustavo"
    templates = boas_vindas(nome=nome_usuario)
    assert "assunto" in templates
    assert "corpo" in templates
    assert nome_usuario in templates["corpo"]

def test_recuperacao_senha_contem_link():
    nome_usuario = "Maria Elizabth"
    link_teste = "https://exemplo.com/recuperar-senha"
    templates = recuperacao_senha(nome=nome_usuario, link=link_teste)
    assert link_teste in templates["corpo"]

def test_confirmacao_pedido_contem_valor():
    nome_usuario = "Marcelo"
    numero_pedido = "12345"
    valor = 99.99
    texto_valor_esperado = "R$99.99"
    templates = confirmacao_pedido(nome=nome_usuario, numero_pedido=numero_pedido, valor=valor)
    assert numero_pedido in templates["corpo"]
    assert texto_valor_esperado in templates["corpo"]