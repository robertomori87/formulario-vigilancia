from fpdf import FPDF
import tempfile
import base64
import json
from io import BytesIO
from datetime import datetime

def gerar_pdf(dados_envio):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Checklist - LTA Saneantes", ln=True, align='C')
    pdf.ln(10)

    def linha_rotulo_valor(rotulo, valor):
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(60, 10, f"{rotulo}:", ln=0)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, valor if valor else "-")

    for campo in [
        "tipo_pessoa", "razao_social", "cnpj", "nome_pf", "cpf_pf",
        "logradouro", "numero", "bairro", "cep", "cidade",
        "nome_rt", "cpf_rt", "nome_rl", "cpf_rl"
    ]:
        linha_rotulo_valor(campo.replace("_", " ").upper(), str(dados_envio.get(campo, "-")))

    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Respostas:", ln=True)

    respostas = json.loads(dados_envio.get("respostas", "[]"))
    for r in respostas:
        pdf.set_font("Arial", style="B", size=12)
        pdf.multi_cell(0, 10, f"{r['id']}. {r['pergunta']}")
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Resposta: {r['resposta']}", ln=True)
        if r["justificativa"]:
            pdf.multi_cell(0, 10, f"Justificativa: {r['justificativa']}")
        if r["comentario"]:
            pdf.multi_cell(0, 10, f"Comentário: {r['comentario']}")
        pdf.ln(3)

    pdf.ln(10)

    meses_pt = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    hoje = datetime.now()
    data_formatada = f"Sertãozinho - SP, {hoje.day} de {meses_pt[hoje.month - 1]} de {hoje.year}"
    pdf.cell(0, 10, data_formatada, ln=True, align='C')


    pdf.ln(15)
    pdf.cell(0, 10, "Assinatura do Responsável Legal", ln=True, align='C')
    pdf.cell(0, 10, dados_envio.get("nome_rl", "-"), ln=True, align='C')

    pdf.ln(15)
    pdf.cell(0, 10, "Assinatura do Responsável Técnico", ln=True, align='C')
    pdf.cell(0, 10, dados_envio.get("nome_rt", "-"), ln=True, align='C')

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer