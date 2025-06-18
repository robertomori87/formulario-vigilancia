# src_formulario/criar_tabelas.py

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Usa a string de conexão definida no .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Caminho seguro e absoluto para o arquivo SQL
import_path = os.path.join(os.path.dirname(__file__), 'sql', 'checklist_projeto.sql')

with open(import_path, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Executa o script no banco de dados
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Criando estrutura do banco de dados...")
    conn.execute(text(sql_script))
    print("✅ Estrutura criada com sucesso.")
