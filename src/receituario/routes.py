# src/receituario/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, send_file, jsonify
from src.common.database import SessionLocal, SolicitacaoReceituario
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
import random

receituario_bp = Blueprint("receituario_bp", __name__)

PDF_DIR = "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)


def gerar_protocolo():
    """Gera um número de protocolo no formato REC_YYMMDDXXX."""
    agora = datetime.now()
    data_formatada = agora.strftime("%y%m%d")
    ordem_diaria = random.randint(1, 999)
    ordem_diaria_str = f"{ordem_diaria:03d}"
    return f"REC_{data_formatada}{ordem_diaria_str}"


@receituario_bp.route("/")
def index():
    """Renderiza a página inicial."""
    return render_template("index.html")


@receituario_bp.route("/login", methods=["GET", "POST"])
def login():
    """Lida com a autenticação de login."""
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == "admin" and senha == "12345": # Lembre-se de melhorar esta autenticação em produção!
            session["logado"] = True
            return redirect(url_for("receituario_bp.consultar"))
        else:
            return "Usuário ou senha incorretos."
    return render_template("login.html")



@receituario_bp.route("/logout")
def logout():
    session.pop("logado", None)
    return redirect(url_for("receituario_bp.login"))


@receituario_bp.route("/enviar", methods=["POST"])
def enviar():
    try:
        form = request.form
        protocolo = gerar_protocolo()
        data_geracao = datetime.now().date()
        hora_geracao = datetime.now().time()
        db = SessionLocal()

        has_third_party = form.get("has_third_party")
        nome_terceiro_val = form.get("nome_terceiro") if has_third_party == "yes" else "---"
        cpf_terceiro_val = form.get("cpf_terceiro") if has_third_party == "yes" else "---"

        nova_solicitacao = SolicitacaoReceituario(
            nome=form.get("nome"),
            cpf_cnpj=form.get("cpf_cnpj"),
            telefone=form.get("telefone"),
            responsavel=form.get("responsavel"),
            conselho=form.get("conselho"),
            numero_conselho=form.get("numero_conselho"),
            endereco=form.get("endereco"),
            nome_terceiro=nome_terceiro_val,
            cpf_terceiro=cpf_terceiro_val,
            receita_a=form.get("receita_a"),
            receita_b=form.get("receita_b"),
            receita_b2=form.get("receita_b2"),
            retinoides=form.get("retinoides"),
            talidomida=form.get("talidomida"),
            protocolo=protocolo,
            data_protocolo=data_geracao,
            hora_protocolo=hora_geracao
        )

        db.add(nova_solicitacao)
        db.commit()
        db.close()

        # PDF
        pdf_path = os.path.join(PDF_DIR, f"{protocolo}.pdf")
        pdf = canvas.Canvas(pdf_path, pagesize=A4)
        pdf.drawString(100, 800, f"Protocolo: {protocolo}")
        pdf.save()

        return render_template("sucesso.html", protocolo=protocolo)

    except SQLAlchemyError as e:
        db.rollback()
        return f"Erro no banco: {str(e)}", 500
    except Exception as e:
        return f"Erro inesperado: {str(e)}", 500


@receituario_bp.route("/baixar/<protocolo>")
def baixar_pdf(protocolo):
    path = os.path.join(PDF_DIR, f"{protocolo}.pdf")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Arquivo não encontrado", 404


@receituario_bp.route("/consultar")
def consultar():
    if not session.get("logado"):
        return redirect(url_for("receituario_bp.login"))
    db = SessionLocal()
    registros = db.query(SolicitacaoReceituario).order_by(SolicitacaoReceituario.id.desc()).all()
    db.close()
    return render_template("consulta.html", registros=registros)


@receituario_bp.route("/deletar_solicitacoes", methods=["POST"])
def deletar_solicitacoes():
    if not session.get("logado"):
        return redirect(url_for("receituario_bp.login"))
    selected_ids = [int(id) for id in request.json.get("ids", [])]
    db = SessionLocal()
    try:
        db.execute(delete(SolicitacaoReceituario).where(SolicitacaoReceituario.id.in_(selected_ids)))
        db.commit()
        return {"message": f"{len(selected_ids)} solicitações deletadas."}, 200
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 500
    finally:
        db.close()


