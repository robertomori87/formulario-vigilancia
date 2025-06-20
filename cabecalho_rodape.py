from fpdf import FPDF
from datetime import datetime
import os

def adicionar_cabecalho(pdf: FPDF):
    pdf.set_y(5)
    caminho_logo = os.path.join(os.path.dirname(__file__), "logo_sertaozinho_quadrado.jpeg")
    
    if os.path.exists(caminho_logo):
        pdf.image(caminho_logo, x=10, y=5, w=20)

    pdf.set_xy(0, 6)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(0)
    pdf.cell(0, 5, "PREFEITURA MUNICIPAL DE SERTÃOZINHO", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "SECRETARIA MUNICIPAL DE SAÚDE", ln=True, align='C')
    pdf.cell(0, 5, "VIGILÂNCIA SANITÁRIA", ln=True, align='C')

    pdf.set_line_width(0.5)
    pdf.line(10, 25, 200, 25)
    pdf.ln(10)


def adicionar_rodape(pdf: FPDF, pagina_atual: int):
    pdf.set_line_width(0.5)
    pdf.line(10, 277, 200, 277)

    pdf.set_y(-22)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 5, f"Página {pagina_atual} / {{nb}}", ln=True, align="C")

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 5, f"Documento gerado eletronicamente em {data_hoje}", ln=True, align="C")
    pdf.cell(0, 5, "Preenchido pelo requerente", ln=True, align="C")
    pdf.cell(0, 5, "Vigilância Sanitária de Sertãozinho-SP.", ln=True, align="C")