import streamlit as st
import pandas as pd
import json
from supabase import create_client
import os
import re
from gerar_pdf import gerar_pdf

# --- Antiga parte do st.set_page_config e st.title, agora dinâmica ---
st.set_page_config(page_title="Laudo Técnico de Avaliação", layout="wide")

# --- Fim da modificação ---

# --- Nova parte: Seleção da Atividade e Carregamento do JSON ---
@st.cache_data
def carregar_dados_atividade(json_filename):
    """
    Carrega os dados de um arquivo JSON específico, incluindo o nome da atividade
    e as perguntas.
    """
    json_path = os.path.join(os.path.dirname(__file__), json_filename)
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{json_filename}' não foi encontrado.")
        st.stop() # Para a execução do app se o arquivo não for encontrado
    except json.JSONDecodeError:
        st.error(f"Erro: O arquivo '{json_filename}' não é um JSON válido.")
        st.stop()

# Mapeamento dos tipos de atividade para seus respectivos arquivos JSON
# Você pode expandir isso para incluir mais arquivos JSON conforme criar
atividades_disponiveis = {
    "INDÚSTRIA DE SANEANTES DOMISSANITÁRIOS": "checklist_saneantes_domissanitarios.json",
    #"INDÚSTRIA DE ALIMENTOS": "checklist_alimentos.json",
    # Adicione mais aqui:
    # "INDÚSTRIA DE COSMÉTICOS": "checklist_cosmeticos.json",
}

# Permite ao usuário selecionar a atividade
# O valor padrão pode ser ajustado para a atividade mais comum ou a primeira da lista
atividade_selecionada_nome = st.sidebar.selectbox(
    "Selecione o tipo de atividade:",
    list(atividades_disponiveis.keys()),
    index=0 # Define a primeira opção como padrão
)



# Pega o nome do arquivo JSON correspondente à atividade selecionada
nome_do_arquivo_json = atividades_disponiveis[atividade_selecionada_nome]

# Carrega os dados do JSON da atividade selecionada
dados_atividade = carregar_dados_atividade(nome_do_arquivo_json)

# Extrai o nome da atividade e as perguntas
nome_da_atividade = dados_atividade["nome_atividade"]
df = pd.DataFrame(dados_atividade["perguntas"])
# --- Fim da nova parte ---

st.title(f"Laudo Técnico de Avaliação - {nome_da_atividade}")


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

def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf

def formatar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}" if len(cnpj) == 14 else cnpj

def validar_cep(cep: str) -> bool:
    return bool(re.fullmatch(r"\d{5}-?\d{3}", cep))

def formatar_cep(cep):
    cep = ''.join(filter(str.isdigit, cep))
    return f"{cep[:5]}-{cep[5:]}" if len(cep) == 8 else cep

# Leitura da planilha
# Carrega o JSON (estando na mesma pasta do app)
# @st.cache_data
# def carregar_perguntas():
#     json_path = os.path.join(os.path.dirname(__file__), "checklist_perguntas.json")
#     with open(json_path, encoding="utf-8") as f:
#         return pd.DataFrame(json.load(f))

# df = carregar_perguntas()

# st.write("DEBUG: JSON carregado com sucesso! Número de linhas no DataFrame:", len(df))

# # Carrega os dados do JSON em um DataFrame
# with open(json_path, encoding="utf-8") as f:
#     dados_json = json.load(f)
# df = pd.DataFrame(dados_json)


# Antes da bifurcação
razao_social = ""
cnpj = ""
nome_pf = ""
cpf_pf = ""

mensagem_cpf = "CPF (somente números)"
ajuda_cpf = "Ex: 12345678901 ou 123.456.789-01"

mensagem_cnpj = "CNPJ (somente números)"
ajuda_cnpj = "Ex: 12345678000195 ou 12.345.678/0001-95"

mensagem_cep = "CEP (formato XXXXX-XXX)"
ajuda_cep = "Ex: 14020-000"

st.markdown("Preencha todos os dados do formulário abaixo.")

st.header("Identificação do Estabelecimento")


# Pessoa física ou jurídica
tipo_pessoa = st.radio("Tipo de Pessoa:", ["Pessoa Jurídica", "Pessoa Física"], horizontal=True)

if tipo_pessoa == "Pessoa Jurídica":
    col1, col2 = st.columns(2)
    with col1:
        razao_social = st.text_input("Razão Social").upper()
    with col2:
        cnpj = st.text_input(mensagem_cnpj, help=ajuda_cnpj)
else:
    col1, col2 = st.columns(2)
    with col1:
        nome_pf = st.text_input("Nome completo").upper()
    with col2:
        cpf_pf = st.text_input(mensagem_cpf, help=ajuda_cpf, key="cpf_pf")


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
    logradouro_tipo = st.selectbox("Tipo de logradouro:", tipos_logradouro)
    logradouro_tipo = logradouro_tipo.upper()
with col2:
    logradouro = st.text_input("Logradouro").upper()
with col3:
    numero = st.text_input("Número")

col1, col2 = st.columns(2)
with col1:
    bairro = st.text_input("Bairro").upper()
with col2:
    cep = st.text_input(mensagem_cep, help=ajuda_cep)

cidade = "SERTÃOZINHO-SP"
st.text_input("Cidade", value=cidade, disabled=True)

st.subheader("Responsável Técnico pelo Projeto")
col1, col2 = st.columns(2)
with col1:
    nome_rt = st.text_input("Nome do RT").upper()
with col2:
    cpf_rt = st.text_input(mensagem_cpf, help=ajuda_cpf, key="cpf_rt")

st.subheader("Responsável Legal")
col1, col2 = st.columns(2)
with col1:
    nome_rl = st.text_input("Nome do Responsável Legal").upper()
with col2:
    cpf_rl = st.text_input(mensagem_cpf, help=ajuda_cpf, key="cpf_rl")

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
        # Montagem dos dados
        dados_envio = {
            "tipo_pessoa": tipo_pessoa,
            "razao_social": razao_social if tipo_pessoa == "Pessoa Jurídica" else None,
            "cnpj": formatar_cnpj(cnpj) if tipo_pessoa == "Pessoa Jurídica" else None,
            "nome_pf": nome_pf if tipo_pessoa == "Pessoa Física" else None,
            "cpf_pf": formatar_cpf(cpf_pf) if tipo_pessoa == "Pessoa Física" else None,
            "logradouro": f"{logradouro_tipo or ''} {logradouro}".strip(),
            "numero": numero,
            "bairro": bairro,
            "cep": formatar_cep(cep),
            "cidade": cidade,
            "nome_rt": nome_rt,
            "cpf_rt": formatar_cpf(cpf_rt),
            "nome_rl": nome_rl,
            "cpf_rl": formatar_cpf(cpf_rl),
            "respostas": json.dumps(respostas),
            "atividade": nome_da_atividade # Adicionamos o nome da atividade aqui
        }
        

        try:
            supabase.table("checklist_lta_respostas").insert(dados_envio).execute()
            st.success("✅ Checklist enviado com sucesso!")

            pdf_buffer = gerar_pdf(dados_envio)

            st.download_button(
                label="📥 Baixar PDF preenchido",
                data=pdf_buffer,
                file_name=f"laudo_{nome_da_atividade.replace(' ', '_').lower()}.pdf", # Nome do PDF também dinâmico
                mime="application/pdf"
            )

        except Exception as e:
            st.error("❌ Houve um erro ao salvar os dados. Tente novamente mais tarde.")
            st.caption(f"Erro técnico (para depuração): {e}")




