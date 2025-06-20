from fpdf import FPDF
from datetime import datetime
import os

def adicionar_cabecalho(pdf: FPDF):
    caminho_logo = os.path.join(os.path.dirname(__file__), "logo_sertaozinho_quadrado.jpeg")
    
    altura_linha = 6
    largura_total = 190
    largura_coluna = largura_total / 3

    pdf.set_text_color(0, 0, 0)
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
    
    pdf.set_line_width(0.5)
    pdf.line(10, 277, 200, 277)  # Linha um pouco mais para cima (antes: 277)

    pdf.set_y(-15)  # Também sobe a posição do texto
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "I", 8)

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    rodape_texto = f"Página {pagina_atual} / {{nb}} - Documento preenchido pelo requerente e gerado eletronicamente em {data_hoje}"

    pdf.multi_cell(0, 5, rodape_texto, align="C")