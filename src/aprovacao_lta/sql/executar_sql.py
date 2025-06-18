import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Caminho do arquivo SQL
SQL_FILE = os.path.join(os.path.dirname(__file__), "sql", "checklist_projeto.sql")

# Conexão com o banco
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("⚠️ DATABASE_URL não está definida no .env")

def executar_sql():
    try:
        # Lê o conteúdo do arquivo SQL
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            sql_script = f.read()

        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql_script))

        print("✅ Script SQL executado com sucesso.")

    except FileNotFoundError:
        print(f"❌ Arquivo SQL não encontrado: {SQL_FILE}")
    except Exception as e:
        print(f"❌ Erro ao executar SQL: {e}")

if __name__ == "__main__":
    executar_sql()
