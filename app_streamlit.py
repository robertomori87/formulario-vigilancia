import streamlit as st
import pandas as pd
import json
from supabase import create_client
import os
from gerar_pdf import gerar_pdf

st.set_page_config(page_title="Laudo Técnico de Avaliação - INDÚSTRIA DE SANEANTES DOMISSANITÁRIOS", layout="wide")
st.title("Laudo Técnico de Avaliação - INDÚSTRIA DE SANEANTES DOMISSANITÁRIOS")

def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma2 * 10 % 11) % 10
    return cpf[-2:] == f"{d1}{d2}"

def validar_cnpj(cnpj: str) -> bool:
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1
    soma1 = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    d1 = 11 - soma1 % 11
    d1 = d1 if d1 < 10 else 0
    soma2 = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    d2 = 11 - soma2 % 11
    d2 = d2 if d2 < 10 else 0
    return cnpj[-2:] == f"{d1}{d2}"


# Leitura da planilha
# Carrega o JSON (estando na mesma pasta do app)
@st.cache_data
def carregar_perguntas():
    json_path = os.path.join(os.path.dirname(__file__), "checklist_perguntas.json")
    with open(json_path, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

df = carregar_perguntas()

# st.write("DEBUG: JSON carregado com sucesso! Número de linhas no DataFrame:", len(df))

# # Carrega os dados do JSON em um DataFrame
# with open(json_path, encoding="utf-8") as f:
#     dados_json = json.load(f)
# df = pd.DataFrame(dados_json)




st.markdown("Preencha todos os dados do formulário abaixo.")

st.header("Identificação do Estabelecimento")


# Pessoa física ou jurídica
tipo_pessoa = st.radio("Tipo de Pessoa:", ["Pessoa Jurídica", "Pessoa Física"], horizontal=True)

if tipo_pessoa == "Pessoa Jurídica":
    col1, col2 = st.columns(2)
    with col1:
        razao_social = st.text_input("Razão Social").upper()
    with col2:
        cnpj = st.text_input("CNPJ")
else:
    col1, col2 = st.columns(2)
    with col1:
        nome_pf = st.text_input("Nome completo").upper()
    with col2:
        cpf_pf = st.text_input("CPF")

st.subheader("Endereço do Estabelecimento")

tipos_logradouro = [
    "Avenida", "Rua", "Alameda", "Estrada", "Rodovia", "Quadra", "Travessa", "Residencial", "Aeroporto", "Área",
    "Campo", "Chácara", "Colônia", "Condomínio", "Conjunto", "Distrito", "Esplanada", "Estação", "Favela",
    "Fazenda", "Feira", "Jardim", "Ladeira", "Lago", "Lagoa", "Largo", "Loteamento", "Morro", "Núcleo",
    "Parque", "Passarela", "Pátio", "Praça", "Recanto", "Setor", "Sítio", "Trecho", "Trevo", "Vale",
    "Vereda", "Via", "Viaduto", "Viela", "Vila", "Outros"
]

col1, col2, col3 = st.columns(3)
with col1:
    logradouro_tipo = st.selectbox("Tipo de logradouro:", tipos_logradouro).upper()
with col2:
    logradouro = st.text_input("Logradouro").upper()
with col3:
    numero = st.text_input("Número")

col1, col2 = st.columns(2)
with col1:
    bairro = st.text_input("Bairro").upper()
with col2:
    cep = st.text_input("CEP")

cidade = "SERTÃOZINHO-SP"
st.text_input("Cidade", value=cidade, disabled=True)

st.subheader("Responsável Técnico pelo Projeto")
col1, col2 = st.columns(2)
with col1:
    nome_rt = st.text_input("Nome do RT").upper()
with col2:
    cpf_rt = st.text_input("CPF do RT")

st.subheader("Responsável Legal")
col1, col2 = st.columns(2)
with col1:
    nome_rl = st.text_input("Nome do Responsável Legal").upper()
with col2:
    cpf_rl = st.text_input("CPF do Responsável Legal")

st.subheader("Questionário")

respostas = []

for idx, row in df.iterrows():
    fluxo = str(row["observacao_fluxo"]).strip().upper()
    pergunta_limpa = str(row['pergunta']).replace("**", "").strip()
    with st.expander(f"**{idx+1}. {pergunta_limpa}**"):
        st.markdown(f"📘 **Texto Legal:** {row['texto_legal']}")
        st.markdown(f"⚖️ **Interpretação:** {row['interpretacao_legal']}")
        st.markdown(f"🖼️ **Documentação gráfica:** {row['orientacao_documentacao']}")
        st.markdown(f"📚 **Base legal:** {row['base_legal']}")

        if fluxo == "SIM":
            st.markdown("🧭 **Avaliação:** Este item será avaliado em projeto.")
        else:
            st.markdown(
                "🧭 **Avaliação:** Este item **não é avaliado em projeto**, será verificado em inspeção.",
                help="Item não é avaliado em projeto, será verificado em inspeção."
            )
        
        resposta = st.radio(
            "Selecione uma opção:",
            ["Atende", "Não atende", "Não se aplica (Não realiza a atividade)"],
            index=0,  # Atende será o valor padrão
            key=f"resposta_{idx}"
        )

        justificativa = ""
        if resposta == "Não atende":
            justificativa = st.text_area("✍️ Justifique ou descreva medida mitigatória", key=f"just_{idx}")

        comentario = st.text_input("💬 Comentário do requerente (opcional)", key=f"com_{idx}")
        
        respostas.append({
            "id": idx+1,
            "pergunta": row["pergunta"],
            "resposta": resposta,
            "justificativa": justificativa,
            "comentario": comentario
        })

st.markdown("---")

# ✅ Texto de responsabilidade
st.markdown(
    """
    <div style='font-size: 0.9rem; text-align: justify; color: #444; background-color: #f9f9f9; padding: 10px; border-left: 4px solid #999; margin-bottom: 10px;'>
    <strong>Declaração:</strong> Assumo a inteira responsabilidade pela veracidade das informações aqui prestadas para o exercício das atividades relacionadas e declaro estar ciente da obrigação de prestar esclarecimentos e observar as exigências legais que vierem a ser determinadas pelo órgão de vigilância sanitária competente, em qualquer tempo, na forma prevista no art. 95 da Lei Estadual 10.083 de 23 de setembro de 1998. <br><br>
    <em>Este instrumento não impede outra solicitação por parte da Vigilância Sanitária.</em>
    </div>
    """,
    unsafe_allow_html=True
)

# Conecte ao Supabase
@st.cache_resource
def conectar_supabase():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        st.error("❌ As credenciais do Supabase (URL ou KEY) não estão configuradas corretamente.")
        st.stop()

    return create_client(url, key)

supabase = conectar_supabase()

if st.button("📤 Enviar checklist"):
    erros = []

    # Validação de CPF/CNPJ
    if tipo_pessoa == "Pessoa Jurídica" and not validar_cnpj(cnpj):
        erros.append("❌ CNPJ inválido.")
    if tipo_pessoa == "Pessoa Física" and not validar_cpf(cpf_pf):
        erros.append("❌ CPF da pessoa física inválido.")
    if not validar_cpf(cpf_rt):
        erros.append("❌ CPF do responsável técnico inválido.")
    if not validar_cpf(cpf_rl):
        erros.append("❌ CPF do responsável legal inválido.")

    if tipo_pessoa == "Pessoa Jurídica" and not razao_social:
        erros.append("❌ Razão social não preenchida.")
    if tipo_pessoa == "Pessoa Física" and not nome_pf:
        erros.append("❌ Nome da pessoa física não preenchido.")
    if not logradouro or not numero or not bairro or not cep:
        erros.append("❌ Endereço incompleto.")

    razao_social = cnpj = nome_pf = cpf_pf = ""  # evita NameError

    # Validação das respostas do checklist
    for r in respostas:
        if not r["resposta"]:
            erros.append(f"❌ Item {r['id']} - resposta não preenchida.")
        elif r["resposta"] == "Não atende" and not r["justificativa"].strip():
            erros.append(f"⚠️ Item {r['id']} - justificativa obrigatória.")

    if erros:
        st.error("Erros encontrados:")
        for erro in erros:
            st.markdown(f"- {erro}")
    else:
        # Dados que serão enviados ao Supabase
        dados_envio = {
            "tipo_pessoa": tipo_pessoa,
            "razao_social": razao_social if tipo_pessoa == "Pessoa Jurídica" else None,
            "cnpj": cnpj if tipo_pessoa == "Pessoa Jurídica" else None,
            "nome_pf": nome_pf if tipo_pessoa == "Pessoa Física" else None,
            "cpf_pf": cpf_pf if tipo_pessoa == "Pessoa Física" else None,
            "logradouro": f"{logradouro_tipo or ''} {logradouro}".strip(),
            "numero": numero,
            "bairro": bairro,
            "cep": cep,
            "cidade": cidade,
            "nome_rt": nome_rt,
            "cpf_rt": cpf_rt,
            "nome_rl": nome_rl,
            "cpf_rl": cpf_rl,
            "respostas": json.dumps(respostas)  # envia como string JSON
        }

        try:
            supabase.table("checklist_lta_respostas").insert(dados_envio).execute()
            st.success("✅ Checklist enviado com sucesso!")

            pdf_buffer = gerar_pdf(dados_envio)
            st.download_button("📥 Baixar PDF preenchido", data=pdf_buffer, file_name="checklist_lta.pdf", mime="application/pdf")
        except Exception as e:
            st.error("❌ Houve um erro ao salvar os dados. Tente novamente mais tarde.")
            st.caption(f"Erro técnico (para depuração): {e}")

        # st.success("✅ Checklist validado com sucesso (dados não foram enviados ainda).")
        # st.json(dados_envio)  # Mostra os dados simulados na tela para teste

# if st.button("📤 Enviar checklist"):
#     st.success("✅ Checklist validado com sucesso (dados não foram enviados ainda).")
#     st.json(dados_envio)  # Mostra os dados simulados na tela para teste


