from fpdf import FPDF
from datetime import datetime
import os

def adicionar_cabecalho(pdf: FPDF):
    pdf.set_y(5)  # Posição fixa no topo
    caminho_logo = os.path.join(os.path.dirname(__file__), "logo_sertaozinho_quadrado.jpeg")
    
    if os.path.exists(caminho_logo):
        pdf.image(caminho_logo, x=10, y=5, w=20)  # logotipo à esquerda
    
    pdf.set_xy(35, 6)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 5, "PREFEITURA MUNICIPAL DE SERTÃOZINHO", ln=True)
    pdf.set_x(35)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "SECRETARIA MUNICIPAL DE SAÚDE", ln=True)
    pdf.set_x(35)
    pdf.cell(0, 5, "VIGILÂNCIA SANITÁRIA", ln=True)

    # Linha separadora
    pdf.set_line_width(0.5)
    pdf.line(x1=10, y1=25, x2=200, y2=25)

    pdf.ln(10)  # Pequeno espaço após a linha

def adicionar_rodape(pdf: FPDF, pagina_atual: int, total_paginas: int):
    # Linha separadora
    pdf.set_line_width(0.5)
    pdf.line(x1=10, y1=277, x2=200, y2=277)

    # Posiciona o texto logo acima do limite inferior da página
    pdf.set_y(-25)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 5, f"Página {pagina_atual} / {total_paginas}", ln=True, align="C")
    
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 5, f"Documento gerado eletronicamente em {data_hoje}", ln=True, align="C")
    pdf.cell(0, 5, "Preenchido pelo requerente", ln=True, align="C")
    pdf.cell(0, 5, "Vigilância Sanitária de Sertãozinho-SP.", ln=True, align="C")