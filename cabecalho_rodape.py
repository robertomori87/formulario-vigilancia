from fpdf import FPDF
from datetime import datetime
import os

def adicionar_cabecalho(pdf: FPDF):
    caminho_logo = os.path.join(os.path.dirname(__file__), "logo_sertaozinho_quadrado.jpeg")
    
    altura_linha = 6
    largura_total = 190
    largura_coluna = largura_total / 3

    pdf.set_y(5)
    pdf.set_font("Arial", "B", 11)

    # Linha com 3 colunas (imagem, texto, vazio para balancear)
    pdf.set_xy(10, 5)
    
    # Coluna 1: Imagem
    if os.path.exists(caminho_logo):
        pdf.image(caminho_logo, x=10, y=6, w=20)

    # Coluna 2: Texto centralizado
    pdf.set_xy(10 + largura_coluna, 6)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(largura_coluna, altura_linha, "PREFEITURA MUNICIPAL DE SERTÃOZINHO", ln=1, align='C')

    pdf.set_x(10 + largura_coluna)
    pdf.set_font("Arial", "", 10)
    pdf.cell(largura_coluna, altura_linha, "SECRETARIA MUNICIPAL DE SAÚDE", ln=1, align='C')

    pdf.set_x(10 + largura_coluna)
    pdf.cell(largura_coluna, altura_linha, "VIGILÂNCIA SANITÁRIA", ln=1, align='C')

    # Linha divisória inferior
    pdf.set_line_width(0.5)
    pdf.line(10, 25, 200, 25)
    pdf.ln(10)


def adicionar_rodape(pdf: FPDF, pagina_atual: int):
    linha_y = 282  # linha mais para cima
    pdf.set_line_width(0.5)
    pdf.line(10, linha_y, 200, linha_y)

    pdf.set_y(linha_y + 2)  # onde começam os textos abaixo da linha
    pdf.set_font("Arial", "I", 8)

    # Número da página abaixo da linha
    pdf.cell(0, 5, f"Página {pagina_atual} / {{nb}}", ln=True, align="C")

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 5, f"Documento gerado eletronicamente em {data_hoje}", ln=True, align="C")
    pdf.cell(0, 5, "Preenchido pelo requerente", ln=True, align="C")
    pdf.cell(0, 5, "Vigilância Sanitária de Sertãozinho-SP.", ln=True, align="C")