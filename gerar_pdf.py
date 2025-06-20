from fpdf import FPDF
from io import BytesIO
from datetime import datetime
import json
import re
from cabecalho_rodape import adicionar_cabecalho, adicionar_rodape

# Definir a variável para o nome da fonte
FONT_NAME = "Arial" # Usando Arial para compatibilidade total e evitar erros de fonte
# Se você quiser tentar novamente com DejaVuSans, você mudaria aqui para "DejaVuSans"
# e reintroduziria os add_font no __init__ (com os arquivos .ttf no lugar).

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.alias_nb_pages()  # <-- aqui
        self.set_auto_page_break(auto=True, margin=25)
        self.set_font(FONT_NAME, size=10)
        self.add_page()

    def header(self):
        adicionar_cabecalho(self)

    def footer(self):
        adicionar_rodape(self, self.page_no())

def gerar_ultima_pagina(pdf: FPDF, nome_rl: str, nome_rt: str):
    from datetime import datetime

    # Adiciona nova página
    pdf.add_page()
    pdf.set_y(50)

    # Data formatada (ex: Sertãozinho - SP, 20 de junho de 2025)
    meses_pt = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    hoje = datetime.now()
    data_formatada = f"Sertãozinho - SP, {hoje.day} de {meses_pt[hoje.month - 1]} de {hoje.year}"

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, data_formatada, ln=True, align='C')
    pdf.ln(20)

    # Assinatura do Responsável Legal
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 5, "___________________________________", ln=True, align='C')
    pdf.cell(0, 10, "Assinatura do Responsável Legal", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 5, nome_rl or "Nome do Responsável Legal", ln=True, align='C')
    pdf.ln(20)

    # Assinatura do Responsável Técnico
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 5, "___________________________________", ln=True, align='C')
    pdf.cell(0, 10, "Assinatura do Responsável Técnico", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 5, nome_rt or "Nome do Responsável Técnico", ln=True, align='C')
    pdf.ln(20)

    # Espaço reservado para a Prefeitura carimbar (10cm ≈ 283 pontos)
    pdf.ln(10)

    pdf.set_line_width(0.4)
    pdf.set_draw_color(180, 180, 180)
    pdf.set_fill_color(250, 250, 250)

    y_inicio = pdf.get_y()
    pdf.rect(20, y_inicio, 170, 380)  

    pdf.set_y(y_inicio + 3)
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Espaço reservado à Prefeitura para carimbo oficial, assinatura e validação documental.", ln=True, align='C')
    pdf.set_y(y_inicio + 95)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 6, "(Não escrever ou colar nada nesta área)", ln=True, align='C')

    # Retorna ao preto
    pdf.set_text_color(0, 0, 0)

def gerar_pdf(dados_envio):
    pdf = PDF()
    
    pdf.set_margins(20, 20, 20)

    # Função para limpar caracteres não suportados por fontes built-in
    def clean_text(text):
        if text is None: # Garante que o texto não é None antes de processar
            return "-"
        text = str(text) # Converte para string explicitamente
        # Substitui a seta por um traço ou apenas remove.
        cleaned_text = text.replace("→", "->")
        return cleaned_text

    # --- Document Title ---
    pdf.set_font(FONT_NAME, style="B", size=20)
    pdf.set_text_color(0, 50, 100)
    pdf.cell(0, 15, txt=clean_text("Relatório de Checklist LTA Saneantes"), ln=True, align='C')
    pdf.ln(10)

    # --- Section: Dados Cadastrais ---
    pdf.set_fill_color(230, 230, 230)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(FONT_NAME, style="B", size=14)
    pdf.cell(0, 10, clean_text("1. Dados Cadastrais"), 0, 1, 'L', 1)
    pdf.ln(5)

    pdf.set_font(FONT_NAME, size=11)
    cadastro_fields = {
        "Tipo de Pessoa": "tipo_pessoa",
        "Razão Social": "razao_social",
        "CNPJ": "cnpj",
        "Nome Completo (PF)": "nome_pf",
        "CPF (PF)": "cpf_pf",
    }
    for label, key in cadastro_fields.items():
        value = clean_text(dados_envio.get(key)) # Usa clean_text diretamente aqui
        pdf.cell(pdf.get_string_width(clean_text(label + ": ")) + 2, 8, txt=clean_text(f"{label}:"), border=0, ln=0, align='L')
        pdf.set_font(FONT_NAME, size=11) # Usa a variável da fonte
        pdf.multi_cell(0, 8, txt=value, border=0, align='L')
        pdf.ln(1)

    pdf.ln(5)

    # --- Section: Endereço ---
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font(FONT_NAME, style="B", size=14)
    pdf.cell(0, 10, clean_text("2. Endereço"), 0, 1, 'L', 1)
    pdf.ln(5)

    endereco_fields = {
        "Logradouro": "logradouro",
        "Número": "numero",
        "Bairro": "bairro",
        "CEP": "cep",
        "Cidade": "cidade",
    }
    pdf.set_font(FONT_NAME, size=11)
    for label, key in endereco_fields.items():
        value = clean_text(dados_envio.get(key)) # Usa clean_text diretamente aqui
        pdf.cell(pdf.get_string_width(clean_text(label + ": ")) + 2, 8, txt=clean_text(f"{label}:"), border=0, ln=0, align='L')
        pdf.set_font(FONT_NAME, size=11) # Usa a variável da fonte
        pdf.multi_cell(0, 8, txt=value, border=0, align='L')
        pdf.ln(1)

    pdf.ln(5)

    # --- Section: Responsáveis ---
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font(FONT_NAME, style="B", size=14)
    pdf.cell(0, 10, clean_text("3. Responsáveis"), 0, 1, 'L', 1)
    pdf.ln(5)

    responsaveis_fields = {
        "Nome do Responsável Técnico": "nome_rt",
        "CPF do Responsável Técnico": "cpf_rt",
        "Nome do Responsável Legal": "nome_rl",
        "CPF do Responsável Legal": "cpf_rl",
    }
    pdf.set_font(FONT_NAME, size=11)
    for label, key in responsaveis_fields.items():
        value = clean_text(dados_envio.get(key)) # Usa clean_text diretamente aqui
        pdf.cell(pdf.get_string_width(clean_text(label + ": ")) + 2, 8, txt=clean_text(f"{label}:"), border=0, ln=0, align='L')
        pdf.set_font(FONT_NAME, size=11) # Usa a variável da fonte
        pdf.multi_cell(0, 8, txt=value, border=0, align='L')
        pdf.ln(1)

    pdf.ln(10)

    # --- Section: Respostas do Checklist ---
    pdf.set_fill_color(200, 220, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(FONT_NAME, style="B", size=16)
    pdf.cell(0, 12, clean_text("4. Respostas do Checklist"), 0, 1, 'C', 1)
    pdf.ln(8)

    try:
        respostas = json.loads(dados_envio.get("respostas", "[]"))
    except Exception:
        respostas = []

    if not respostas:
        pdf.set_font(FONT_NAME, size=12)
        pdf.set_text_color(150, 0, 0)
        pdf.cell(0, 10, clean_text("Nenhuma resposta encontrada."), ln=True, align='C')
    else:
        for i, r in enumerate(respostas):
            pdf.set_font(FONT_NAME, style="B", size=12)
            pdf.set_text_color(0, 0, 100)
            pergunta = clean_text(f"Questão {r.get('id', i+1)}. {r.get('pergunta', 'Pergunta não informada')}")
            pdf.multi_cell(0, 8, pergunta, border='B', align='L')
            pdf.ln(2)

            pdf.set_font(FONT_NAME, size=11)
            pdf.set_text_color(50, 50, 50)

            resposta_texto = clean_text(f"Resposta: {r.get('resposta', '-')}")
            pdf.multi_cell(0, 7, resposta_texto)

            if r.get("justificativa"):
                justificativa = clean_text(f"Justificativa: {r['justificativa']}")
                pdf.multi_cell(0, 7, justificativa)

            if r.get("comentario"):
                comentario = clean_text(f"Comentário: {r['comentario']}")
                pdf.multi_cell(0, 7, comentario)

            pdf.ln(5)

    pdf.ln(15)

    # 🔚 Adiciona a última página com assinaturas e espaço reservado
    nome_rl = clean_text(dados_envio.get("nome_rl", "Responsável Legal"))
    nome_rt = clean_text(dados_envio.get("nome_rt", "Responsável Técnico"))
    gerar_ultima_pagina(pdf, nome_rl, nome_rt)

    buffer = BytesIO()
    pdf.output(buffer)  # 'F' = grava no file-like object
    buffer.seek(0)
    return buffer