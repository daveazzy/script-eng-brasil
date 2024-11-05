import pandas as pd
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO
import textwrap

# Configurações do papel Pimaco 6085
PAGINA_LARGURA = 215.9 * mm   # 215.9 mm
PAGINA_ALTURA = 279.4 * mm    # 279.4 mm
ETIQUETA_LARGURA = 84.67 * mm # Largura da etiqueta
ETIQUETA_ALTURA = 46.56 * mm  # Altura da etiqueta

# Margens e espaçamentos
MARGEM_SUPERIOR = 21.2 * mm    # Margem superior do papel
MARGEM_ESQUERDA = 21.2 * mm    # Margem esquerda do papel
ESPACAMENTO_VERTICAL = 4.8 * mm    # Espaço entre etiquetas na vertical
ESPACAMENTO_HORIZONTAL = 4.8 * mm  # Espaço entre etiquetas na horizontal

# Carrega a planilha de dados, tratando valores nulos
df = pd.read_csv('engBRASILDB.csv').fillna('')

def criar_etiqueta(canvas, x, y, id_usuario, nome, instituicao):
    # Gera o QR code a partir do ID
    qr_img = qrcode.make(f"{id_usuario} - {nome} - {instituicao}")
    buffer = BytesIO()
    qr_img.save(buffer)
    buffer.seek(0)
    qr_img = ImageReader(buffer)
    
    # Define o tamanho do QR code e a posição
    qr_tamanho = 30 * mm  # Reduzido para 30mm
    qr_x = x + 5 * mm
    # Centraliza o QR code verticalmente na etiqueta
    qr_y = y - ETIQUETA_ALTURA + ((ETIQUETA_ALTURA - qr_tamanho) / 2)
    
    # Desenha o QR code
    canvas.drawImage(qr_img, qr_x, qr_y, width=qr_tamanho, height=qr_tamanho)
    
    # Define a posição do texto
    texto_x = qr_x + qr_tamanho + 5 * mm
    # Alinha o texto verticalmente com o centro do QR code
    texto_y = qr_y + (qr_tamanho / 2)
    
    # Converte valores para string e aplica letras maiúsculas
    nome = str(nome).upper()
    instituicao = str(instituicao).upper()
    
    # Limita o nome a duas linhas
    nome_linhas = textwrap.wrap(nome, width=20)[:2]
    
    # Calcula a altura total do texto para centralizar verticalmente
    altura_total_texto = (len(nome_linhas) * 12) + (2 * 10)  # altura do nome + altura da instituição
    texto_y_inicio = texto_y + (altura_total_texto / 4)  # Ajusta o ponto de início do texto
    
    # Desenha o nome
    canvas.setFont("Helvetica-Bold", 10)
    for i, linha in enumerate(nome_linhas):
        canvas.drawString(texto_x, texto_y_inicio - (i * 12), linha)
    
    # Desenha a instituição
    instituicao_linhas = textwrap.wrap(instituicao, width=30)[:2]
    canvas.setFont("Helvetica", 8)
    for i, linha in enumerate(instituicao_linhas):
        y_offset = texto_y_inicio - (len(nome_linhas) * 12) - 5 - (i * 10)
        canvas.drawString(texto_x, y_offset, linha)

# Cria o arquivo PDF
c = canvas.Canvas("etiquetas.pdf", pagesize=(PAGINA_LARGURA, PAGINA_ALTURA))
c.setFillColor(colors.black)

# Variáveis de controle
etiquetas_por_linha = 2
etiquetas_por_coluna = 5
x = MARGEM_ESQUERDA
y = PAGINA_ALTURA - MARGEM_SUPERIOR

# Contador para controle de páginas
contador_etiquetas = 0
etiquetas_por_pagina = etiquetas_por_linha * etiquetas_por_coluna

# Gera as etiquetas
for i, row in df.iterrows():
    if contador_etiquetas >= etiquetas_por_pagina:
        c.showPage()
        contador_etiquetas = 0
        x = MARGEM_ESQUERDA
        y = PAGINA_ALTURA - MARGEM_SUPERIOR
    
    id_usuario = row['id']
    nome = row['name']
    instituicao = row['institution']
    
    criar_etiqueta(c, x, y, id_usuario, nome, instituicao)
    contador_etiquetas += 1
    
    # Controle de posição das etiquetas
    if contador_etiquetas % etiquetas_por_linha == 0:
        # Move para a próxima linha
        x = MARGEM_ESQUERDA
        y -= (ETIQUETA_ALTURA + ESPACAMENTO_VERTICAL)
    else:
        # Move para a próxima coluna
        x += ETIQUETA_LARGURA + ESPACAMENTO_HORIZONTAL

# Salva o PDF
c.save()
print("Arquivo 'etiquetas.pdf' gerado com sucesso!")