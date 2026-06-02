def boas_vindas(nome: str) -> dict:
    return {
        "assunto": "Bem-vindo ao nosso serviço!",
        "corpo": f"""Olá {nome},
        Seja bem-vindo ao nosso serviço! Estamos felizes em tê-lo conosco.
        
        Atenciosamente,
        Equipe de Suporte"""
    }

def recuperacao_senha(nome: str, link: str) -> dict:
    return {
        "assunto": "Recuperação de senha",
        "corpo": f"""Olá {nome},
        Para recuperar sua senha, por favor clique no seguinte link:
        {link}
        Se você não solicitou a recuperação de senha, por favor ignore este email.
        Atenciosamente,
        Equipe de Segurança"""
    }

def confirmacao_pedido(nome: str, numero_pedido: str, valor: float) -> dict:
    return {
        "assunto": "Confirmação de pedido",
        "corpo": f"""Olá {nome},
        Seu pedido número {numero_pedido} no valor de R${valor:.2f} foi confirmado.
        Obrigado por comprar conosco!
        
        Atenciosamente,
        Equipe de Vendas"""
    }


