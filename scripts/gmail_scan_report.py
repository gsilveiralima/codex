from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

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


def draw_wrapped_text(canvas_obj, text, x_coord, y_coord, max_width, leading=14):
    """Helper to wrap long strings inside the PDF."""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    words = text.split()
    line = ""
    current_y = y_coord
    for word in words:
        test_line = (line + " " + word).strip()
        if stringWidth(test_line, "Helvetica", 11) <= max_width:
            line = test_line
        else:
            canvas_obj.drawString(x_coord, current_y, line)
            current_y -= leading
            line = word
    if line:
        canvas_obj.drawString(x_coord, current_y, line)
        current_y -= leading
    return current_y


def generate_report(output_path="relatorio_varredura_gmail_malware.pdf"):
    """Generate the PDF report summarizing suspicious Gmail activity."""
    canvas_obj = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    canvas_obj.setFont("Helvetica-Bold", 16)
    canvas_obj.drawString(2 * cm, height - 2 * cm, "Relatório de Varredura – Gmail (Malware/Phishing)")
    canvas_obj.setFont("Helvetica", 10)
    canvas_obj.drawString(
        2 * cm, height - 2.6 * cm, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}  (Horário de Brasília)"
    )

    y_coord = height - 3.2 * cm
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(2 * cm, y_coord, "Resumo")
    y_coord -= 0.6 * cm
    canvas_obj.setFont("Helvetica", 11)
    for line in summary_lines:
        y_coord = draw_wrapped_text(canvas_obj, f"- {line}", 2 * cm, y_coord, max_width=16 * cm)

    y_coord -= 0.3 * cm
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(2 * cm, y_coord, "Itens que exigem atenção")
    y_coord -= 0.6 * cm
    canvas_obj.setFont("Helvetica", 11)

    for finding in findings:
        y_coord = draw_wrapped_text(canvas_obj, f"• Assunto: {finding['subject']}", 2 * cm, y_coord, 16 * cm)
        y_coord = draw_wrapped_text(canvas_obj, f"  Remetente: {finding['sender']}", 2 * cm, y_coord, 16 * cm)
        y_coord = draw_wrapped_text(canvas_obj, f"  Data: {finding['date']}", 2 * cm, y_coord, 16 * cm)
        y_coord = draw_wrapped_text(canvas_obj, f"  Observação: {finding['risk']}", 2 * cm, y_coord, 16 * cm)
        y_coord -= 0.2 * cm
        if y_coord < 3 * cm:
            canvas_obj.showPage()
            y_coord = height - 2 * cm
            canvas_obj.setFont("Helvetica", 11)

    y_coord -= 0.3 * cm
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(2 * cm, y_coord, "Próximos passos (recomendado)")
    y_coord -= 0.6 * cm
    canvas_obj.setFont("Helvetica", 11)
    for step in next_steps:
        y_coord = draw_wrapped_text(canvas_obj, step, 2 * cm, y_coord, 16 * cm)

    y_coord -= 0.3 * cm
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(2 * cm, y_coord, "Glossário")
    y_coord -= 0.6 * cm
    canvas_obj.setFont("Helvetica", 11)
    for term, description in glossario:
        y_coord = draw_wrapped_text(canvas_obj, f"{term}: {description}", 2 * cm, y_coord, 16 * cm)

    canvas_obj.showPage()
    canvas_obj.save()
    print(f"Relatório gerado em: {output_path}")


if __name__ == "__main__":
    generate_report()
