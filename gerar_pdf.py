from fpdf import FPDF
from io import BytesIO
from datetime import datetime
import json
import os # Import os for path handling

# Define a path to your fonts directory
# You can change this to where you store your .ttf files
FONT_DIR = "fonts/" # Or "." if fonts are in the same directory as the script

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)

        # --- Load Unicode Font ---
        # Ensure the font file exists at the specified path
        # You might need to adjust the font filename based on what you download
        try:
            self.add_font("DejaVuSans", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"), uni=True)
            self.add_font("DejaVuSans", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), uni=True)
            # If you only have one DejaVuSans.ttf, you might not have a separate Bold file.
            # In that case, fpdf might try to synthesize bold, but a dedicated bold font is better.
            # If DejaVuSans-Bold.ttf doesn't exist, remove this line or provide the correct path.
        except RuntimeError as e:
            print(f"Erro ao carregar fonte DejaVuSans: {e}. Verifique se os arquivos de fonte (.ttf) estão no diretório '{FONT_DIR}'.")
            # Fallback to a standard font if custom font loading fails,
            # but be aware that unicode characters might still cause issues.
            self.set_font("Helvetica", size=10)
            return

        # Set the loaded Unicode font as the default
        self.set_font("DejaVuSans", size=10)

    def header(self):
        self.set_font('DejaVuSans', 'B', 15)
        self.cell(0, 10, "Checklist - LTA Saneantes", 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVuSans', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')

def gerar_pdf(dados_envio):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_margins(20, 20, 20)

    # --- Document Title ---
    pdf.set_font("DejaVuSans", style="B", size=20)
    pdf.set_text_color(0, 50, 100)
    pdf.cell(0, 15, txt="Relatório de Checklist LTA Saneantes", ln=True, align='C')
    pdf.ln(10)

    # --- Section: Dados Cadastrais ---
    pdf.set_fill_color(230, 230, 230)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVuSans", style="B", size=14)
    pdf.cell(0, 10, "1. Dados Cadastrais", 0, 1, 'L', 1)
    pdf.ln(5)

    pdf.set_font("DejaVuSans", size=11)
    cadastro_fields = {
        "Tipo de Pessoa": "tipo_pessoa",
        "Razão Social": "razao_social",
        "CNPJ": "cnpj",
        "Nome Completo (PF)": "nome_pf",
        "CPF (PF)": "cpf_pf",
    }
    for label, key in cadastro_fields.items():
        value = str(dados_envio.get(key) or "-")
        pdf.cell(pdf.get_string_width(label + ": ") + 2, 8, txt=f"{label}:", border=0, ln=0, align='L')
        pdf.set_font("DejaVuSans", size=11)
        pdf.multi_cell(0, 8, txt=value, border=0, align='L')
        pdf.ln(1)

    pdf.ln(5)

    # --- Section: Endereço ---
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("DejaVuSans", style="B", size=14)
    pdf.cell(0, 10, "2. Endereço", 0, 1, 'L', 1)
    pdf.ln(5)

    endereco_fields = {
        "Logradouro": "logradouro",
        "Número": "numero",
        "Bairro": "bairro",
        "CEP": "cep",
        "Cidade": "cidade",
    }
    pdf.set_font("DejaVuSans", size=11)
    for label, key in endereco_fields.items():
        value = str(dados_envio.get(key) or "-")
        pdf.cell(pdf.get_string_width(label + ": ") + 2, 8, txt=f"{label}:", border=0, ln=0, align='L')
        pdf.set_font("DejaVuSans", size=11)
        pdf.multi_cell(0, 8, txt=value, border=0, align='L')
        pdf.ln(1)

    pdf.ln(5)

    # --- Section: Responsáveis ---
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("DejaVuSans", style="B", size=14)
    pdf.cell(0, 10, "3. Responsáveis", 0, 1, 'L', 1)
    pdf.ln(5)

    responsaveis_fields = {
        "Nome do Responsável Técnico": "nome_rt",
        "CPF do Responsável Técnico": "cpf_rt",
        "Nome do Responsável Legal": "nome_rl",
        "CPF do Responsável Legal": "cpf_rl",
    }
    pdf.set_font("DejaVuSans", size=11)
    for label, key in responsaveis_fields.items():
        value = str(dados_envio.get(key) or "-")
        pdf.cell(pdf.get_string_width(label + ": ") + 2, 8, txt=f"{label}:", border=0, ln=0, align='L')
        pdf.set_font("DejaVuSans", size=11)
        pdf.multi_cell(0, 8, txt=value, border=0, align='L')
        pdf.ln(1)

    pdf.ln(10)

    # --- Section: Respostas do Checklist ---
    pdf.set_fill_color(200, 220, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVuSans", style="B", size=16)
    pdf.cell(0, 12, "4. Respostas do Checklist", 0, 1, 'C', 1)
    pdf.ln(8)

    try:
        respostas = json.loads(dados_envio.get("respostas", "[]"))
    except Exception:
        respostas = []

    if not respostas:
        pdf.set_font("DejaVuSans", size=12)
        pdf.set_text_color(150, 0, 0)
        pdf.cell(0, 10, "Nenhuma resposta encontrada.", ln=True, align='C')
    else:
        for i, r in enumerate(respostas):
            pdf.set_font("DejaVuSans", style="B", size=12)
            pdf.set_text_color(0, 0, 100)
            pergunta = f"Questão {r.get('id', i+1)}. {r.get('pergunta', 'Pergunta não informada')}"
            pdf.multi_cell(0, 8, pergunta, border='B', align='L')
            pdf.ln(2)

            pdf.set_font("DejaVuSans", size=11)
            pdf.set_text_color(50, 50, 50)

            resposta_texto = f"Resposta: {r.get('resposta', '-')}"
            pdf.multi_cell(0, 7, resposta_texto)

            if r.get("justificativa"):
                justificativa = f"Justificativa: {r['justificativa']}"
                pdf.multi_cell(0, 7, justificativa)

            if r.get("comentario"):
                comentario = f"Comentário: {r['comentario']}"
                pdf.multi_cell(0, 7, comentario)

            pdf.ln(5)

    pdf.ln(15)

    # --- Signatures and Date ---
    pdf.set_font("DejaVuSans", size=11)
    pdf.set_text_color(0, 0, 0)

    meses_pt = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    hoje = datetime.now()
    data_formatada = f"Sertãozinho - SP, {hoje.day} de {meses_pt[hoje.month - 1]} de {hoje.year}"
    pdf.cell(0, 10, data_formatada, ln=True, align='C')

    pdf.ln(20)

    # Signature lines
    pdf.set_font("DejaVuSans", style="B", size=12)
    pdf.cell(0, 5, "___________________________________", ln=True, align='C')
    pdf.cell(0, 10, "Assinatura do Responsável Legal", ln=True, align='C')
    pdf.set_font("DejaVuSans", size=11)
    pdf.cell(0, 5, str(dados_envio.get("nome_rl", "Nome do Responsável Legal")), ln=True, align='C')

    pdf.ln(15)

    pdf.set_font("DejaVuSans", style="B", size=12)
    pdf.cell(0, 5, "___________________________________", ln=True, align='C')
    pdf.cell(0, 10, "Assinatura do Responsável Técnico", ln=True, align='C')
    pdf.set_font("DejaVuSans", size=11)
    pdf.cell(0, 5, str(dados_envio.get("nome_rt", "Nome do Responsável Técnico")), ln=True, align='C')

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer