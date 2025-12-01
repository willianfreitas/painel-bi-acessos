import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. CONFIGURAÇÃO ---
USUARIOS_PERMITIDOS = {
    "admin": "admin123",
    "diretoria": "powerbi2024",
    "gestor": "senhaforte"
}

# Nome EXATO da sua planilha no Google
NOME_PLANILHA_GOOGLE = "historico_acessos_bi"

# --- 2. FUNÇÕES ---

def conectar_google_sheets():
    """Conecta ao Google Sheets usando os segredos do Streamlit Cloud"""
    # Define as permissões necessárias
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Pega as credenciais que configuraremos no site do Streamlit
    credentials_info = st.secrets["gcp_service_account"]
    
    creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def salvar_log(usuario):
    """Envia os dados para a nuvem"""
    try:
        client = conectar_google_sheets()
        sheet = client.open(NOME_PLANILHA_GOOGLE).sheet1
        
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Adiciona uma nova linha na planilha
        sheet.append_row([data_hora, usuario])
        
    except Exception as e:
        # Se der erro no log, o usuário ainda consegue ver o BI, mas avisamos no console
        print(f"Erro ao salvar log: {e}")

def check_password():
    """Verifica senha (Lógica igual ao anterior)"""
    def password_entered():
        if st.session_state["username"] in USUARIOS_PERMITIDOS and \
           st.session_state["password"] == USUARIOS_PERMITIDOS[st.session_state["username"]]:
            st.session_state["password_correct"] = True
            salvar_log(st.session_state["username"]) # Salva no Google Sheets
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("😕 Usuário ou senha incorretos.")
        return False
    else:
        return True

# --- 3. INTERFACE ---
st.set_page_config(page_title="Portal BI Corporativo", layout="wide")

if check_password():
    st.success(f"Bem-vindo(a), {st.session_state['username']}!")
    st.divider()
    
    power_bi_code = """
    <iframe title="BI 1.7" width="100%" height="800" 
    src="https://app.powerbi.com/reportEmbed?reportId=45a8812a-04fe-41ed-b971-b21aca1570cc&autoAuth=true&ctid=6956cdca-e442-489f-b791-39f5bd690f49" 
    frameborder="0" allowFullScreen="true"></iframe>
    """
    st.components.v1.html(power_bi_code, height=800)
    
    if st.button("Sair"):
        st.session_state["password_correct"] = False
        st.rerun()