import random
import json
from src.notificacoes import templates, servico, sms

class GerenciadorDeNotificacoes:
    def __init__(self):
        self.historico: list[dict] = []

    def notificar_usuario(self, nome: str, email: str, telefone: str) -> dict:
     
        template = templates.boas_vindas(nome)

        email_enviado = servico.enviar_email(email, template["assunto"], template["corpo"])
        
        codigo_aleatorio = str(random.randint(100000, 999999))
        sms_enviado = sms.enviar_codigo_verificacao(telefone, codigo_aleatorio)

        registro = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "email_enviado": email_enviado,
            "sms_enviado": sms_enviado
        }
        self.historico.append(registro)
        return registro

    def reenviar_falhas(self) -> int:
        reenvios = 0
        for registro in self.historico:
            falhou_email = not registro["email_enviado"]
            falhou_sms = not registro["sms_enviado"]
            
            if falhou_email or falhou_sms:
                reenvios += 1
                if falhou_email:
                    template = templates.boas_vindas(registro["nome"])
                    registro["email_enviado"] = servico.enviar_email(registro["email"], template["assunto"], template["corpo"])
                if falhou_sms:
                    codigo_aleatorio = str(random.randint(100000, 999999))
                    registro["sms_enviado"] = sms.enviar_codigo_verificacao(registro["telefone"], codigo_aleatorio)
        return reenvios

    def resumo(self) -> dict:
        total = len(self.historico)
        emails_enviados = sum(1 for r in self.historico if r["email_enviado"])
        sms_enviados = sum(1 for r in self.historico if r["sms_enviado"])
        falhas_email = sum(1 for r in self.historico if not r["email_enviado"])
        falhas_sms = sum(1 for r in self.historico if not r["sms_enviado"])
        
        return {
            "total": total,
            "emails_enviados": emails_enviados,
            "sms_enviados": sms_enviados,
            "falhas_email": falhas_email,
            "falhas_sms": falhas_sms
        }

    def exportar_historico(self, caminho: str):

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.historico, f, ensure_ascii=False, indent=4)