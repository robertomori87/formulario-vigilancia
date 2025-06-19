#!/bin/bash
echo 'Instalando dependências...'
pip install -r requirements.txt
echo 'Criando estrutura do banco...'
python src/aprovacao_lta/sql/criar_tabelas.py
echo 'Importando perguntas...'
python src/aprovacao_lta/sql/importar_perguntas_excel.py
echo 'Iniciando o servidor...'
gunicorn src.app:app
