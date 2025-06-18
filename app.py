from flask import Flask, redirect, url_for
from src.common.database import Base, engine
from src.receituario.routes import receituario_bp
from src.aprovacao_lta.routes import checklist_bp
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

app = Flask(
    __name__,
    static_folder="common/static",          # Caminho do logo e JS global
    template_folder="common/templates"      # Se houver templates globais, senão remova
)
app.secret_key = os.getenv("SECRET_KEY", "chave_inicial_segura")

if app.secret_key == "chave_inicial_segura":
    print("⚠️ Atenção: você está usando a chave secreta padrão. Configure SECRET_KEY no .env para produção.")

# Registro dos Blueprints
app.register_blueprint(receituario_bp, url_prefix="/receituario")
app.register_blueprint(checklist_bp, url_prefix="/projeto")

# Configura a pasta de arquivos estáticos compartilhados
app.static_folder = os.path.join("common", "static")

# Rota raiz redireciona para o checklist de projeto
@app.route("/")
def index():
    return redirect(url_for("checklist_bp.exibir_checklist_projeto"))

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)



