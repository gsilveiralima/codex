from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Findings to include
findings = [
    {
        "subject": "NOTIFICAÇÃO DE BOLETO VENCIDO",
        "sender": "MÚLTIPLA - ASSOCIAÇÃO MÚLTIPLA DE PROTEÇÃO E ASSISTÊNCIA AUTOMOTIVA <financeiro@multiplaprotecao.com>",
        "date": "2025-10-17 15:12 (-03)",
        "risk": "Pressão para pagamento (urgência). Verifique por canal oficial antes de pagar.",
    },
    {
        "subject": "Existe um REEMBOLSO EM CRÉDITOS que ainda não foi validado",
        "sender": "Temu <email@market.temuemail.com>",
        "date": "2025-10-17 13:36 (-03)",
        "risk": "Linguagem de urgência e vários links externos. Potencial phishing.",
    },
    {
        "subject": "PicPay - Sua fatura PicPay Card está fechada.",
        "sender": "PicPay <no-reply@picpay.com>",
        "date": "2025-10-16 15:47 (-03)",
        "risk": "Possui anexo (provável PDF). Baixe/abra apenas pelo app oficial para conferir.",
    },
    {
        "subject": "Gabriel, confirme seu novo dispositivo",
        "sender": "LinkedIn <security-noreply@linkedin.com>",
        "date": "2025-10-17 04:01 (-03)",
        "risk": "Alerta legítimo comum. Se não foi você, troque a senha e revise sessões.",
    },
    {
        "subject": "Gabriel, aqui está seu código 988413",
        "sender": "LinkedIn <security-noreply@linkedin.com>",
        "date": "2025-10-17 04:01 (-03)",
        "risk": "Código 2FA. Se não solicitado por você, possível tentativa de acesso não autorizado.",
    },
    {
        "subject": "(No Subject) [RASCUNHO]",
        "sender": "Gabriel Silveira <g.silveira801@gmail.com>",
        "date": "2024-12-08 11:56 (-03)",
        "risk": "Rascunho seu com anexo. Confirme que reconhece o arquivo e a origem.",
    },
]

summary_lines = [
    "• Nenhum anexo executável de alto risco (.exe, .js, .vbs, .apk etc.) foi encontrado na caixa de entrada nos últimos 2 anos.",
    "• 1 rascunho seu possui anexo — revisar se você reconhece o arquivo.",
    "• 10 mensagens com termos comuns de engenharia social foram encontradas no último ano; 5 exigem atenção.",
]

next_steps = [
    "1) Verificar faturas/boletos no app ou site oficial (PicPay, bancos) antes de abrir anexos.",
    "2) Ativar/verificar 2FA e revisar sessões ativas (ex.: LinkedIn).",
    "3) Desconfiar de urgência, reembolsos inesperados, e links encurtados.",
    "4) Quando em dúvida, encaminhar o anexo para análise offline/antivírus antes de abrir.",
]

glossario = [
    ("Phishing", "Golpe que tenta enganar você para clicar em links ou abrir anexos maliciosos."),
    ("2FA", "Autenticação de dois fatores; exige um segundo código além da senha."),
    ("Anexo executável", "Arquivo que pode rodar código (ex.: .exe/.js/.vbs/.apk)."),
    ("Engenharia social", "Técnicas de persuasão para induzir erro ou ação impulsiva."),
]

def draw_wrapped_text(c, text, x, y, max_width, leading=14):
    """Helper to wrap long strings inside the PDF."""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if stringWidth(test, "Helvetica", 11) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y

def generate_report(output_path="relatorio_varredura_gmail_malware.pdf"):
    """Generate the PDF report summarizing suspicious Gmail activity."""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "Relatório de Varredura – Gmail (Malware/Phishing)")
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 2.6 * cm, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}  (Horário de Brasília)")

    y = height - 3.2 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Resumo")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    for line in summary_lines:
        y = draw_wrapped_text(c, f"- {line}", 2 * cm, y, max_width=16 * cm)

    y -= 0.3 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Itens que exigem atenção")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)

    for finding in findings:
        y = draw_wrapped_text(c, f"• Assunto: {finding['subject']}", 2 * cm, y, 16 * cm)
        y = draw_wrapped_text(c, f"  Remetente: {finding['sender']}", 2 * cm, y, 16 * cm)
        y = draw_wrapped_text(c, f"  Data: {finding['date']}", 2 * cm, y, 16 * cm)
        y = draw_wrapped_text(c, f"  Observação: {finding['risk']}", 2 * cm, y, 16 * cm)
        y -= 0.2 * cm
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica", 11)

    y -= 0.3 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Próximos passos (recomendado)")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    for step in next_steps:
        y = draw_wrapped_text(c, step, 2 * cm, y, 16 * cm)

    y -= 0.3 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Glossário")
    y -= 0.6 * cm
    c.setFont("Helvetica", 11)
    for term, desc in glossario:
        y = draw_wrapped_text(c, f"{term}: {desc}", 2 * cm, y, 16 * cm)

    c.showPage()
    c.save()
    print(f"Relatório gerado em: {output_path}")


if __name__ == "__main__":
    generate_report()
