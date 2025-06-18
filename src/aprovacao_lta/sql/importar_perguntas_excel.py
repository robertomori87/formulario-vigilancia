import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import sys

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.common.database import Base, Checklist

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = os.path.dirname(__file__)
EXCEL_FILE = os.path.join(BASE_DIR, "dados", "checklist_perguntas.xlsx")

def importar_perguntas_do_excel():
    try:
        df = pd.read_excel(EXCEL_FILE)

        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL não configurada no .env")

        engine = create_engine(DATABASE_URL)

        colunas_mapeadas = {
            "Numero_Item": "numero_item",
            "Pergunta": "pergunta",
            "Texto_Legal": "texto_legal",
            "Interpretacao_Legal": "interpretacao_legal",
            "Orientacao_Documentacao": "orientacao_documentacao",
            "Observacao_Fluxo": "observacao_fluxo",
            "Base_Legal": "base_legal"
        }

        # ✅ RENOMEIA as colunas do Excel para bater com o banco
        df = df.rename(columns={k: v for k, v in colunas_mapeadas.items()})

        # ✅ Garante que TODAS existam
        for coluna in colunas_mapeadas.values():
            if coluna not in df.columns:
                df[coluna] = None

        df_import = df[list(colunas_mapeadas.values())]

        print(f"Importando perguntas do Excel: {EXCEL_FILE}")

        with engine.connect() as conn:
            with conn.begin():
                for _, row in df_import.iterrows():
                    dados = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

                    sql = text("""
                        INSERT INTO aprovacao_projeto.checklist (
                            numero_item, pergunta, texto_legal, interpretacao_legal,
                            orientacao_documentacao, base_legal, observacao_fluxo
                        ) VALUES (
                            :numero_item, :pergunta, :texto_legal, :interpretacao_legal,
                            :orientacao_documentacao, :base_legal, :observacao_fluxo
                        ) ON CONFLICT (numero_item) DO UPDATE SET
                            pergunta = EXCLUDED.pergunta,
                            texto_legal = EXCLUDED.texto_legal,
                            interpretacao_legal = EXCLUDED.interpretacao_legal,
                            orientacao_documentacao = EXCLUDED.orientacao_documentacao,
                            base_legal = EXCLUDED.base_legal,
                            observacao_fluxo = EXCLUDED.observacao_fluxo;
                    """)
                    conn.execute(sql, dados)

        print(f"✅ {len(df_import)} perguntas importadas/atualizadas com sucesso.")

    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {EXCEL_FILE}")
    except ValueError as ve:
        print(f"⚠️ Erro de configuração: {ve}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    importar_perguntas_do_excel()
