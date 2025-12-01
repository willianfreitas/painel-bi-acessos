import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURAÇÃO DOS USUÁRIOS ---
# Aqui você define quem pode acessar.
# Formato: "usuario": "senha"
USUARIOS_PERMITIDOS = {
    "admin": "admin123",
    "diretoria": "powerbi2024",
    "gestor": "senhaforte"
}

# Nome do arquivo onde salvaremos os logs
ARQUIVO_LOG = "historico_acessos.csv"

# --- 2. FUNÇÕES DO SISTEMA ---

def salvar_log(usuario):
    """Registra quem acessou e quando em um arquivo CSV."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novo_acesso = pd.DataFrame([[data_hora, usuario]], columns=["Data_Hora", "Usuario"])
    
    # Se o arquivo já existe, adiciona o novo acesso. Se não, cria o arquivo.
    if not os.path.isfile(ARQUIVO_LOG):
        novo_acesso.to_csv(ARQUIVO_LOG, index=False)
    else:
        novo_acesso.to_csv(ARQUIVO_LOG, mode='a', header=False, index=False)

def check_password():
    """Verifica se a senha está correta."""
    def password_entered():
        if st.session_state["username"] in USUARIOS_PERMITIDOS and \
           st.session_state["password"] == USUARIOS_PERMITIDOS[st.session_state["username"]]:
            st.session_state["password_correct"] = True
            # Salva o log apenas quando o login é bem-sucedido
            salvar_log(st.session_state["username"]) 
            del st.session_state["password"]  # Limpa a senha da memória por segurança
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Primeira vez que a página carrega
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Senha incorreta
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("😕 Usuário ou senha incorretos.")
        return False
    else:
        # Senha correta
        return True

# --- 3. INTERFACE (FRONTEND) ---

st.set_page_config(page_title="Portal BI Corporativo", layout="wide")

if check_password():
    # Se o login der certo, mostra o conteúdo abaixo:
    st.success(f"Bem-vindo(a), {st.session_state['username']}!")
    
    st.divider()
    
    st.write("### Painel de Indicadores")
    
    # O SEU CÓDIGO DO POWER BI ENTRA AQUI
    # Ajustei a altura para ficar melhor na tela
    power_bi_code = """
    <iframe title="BI 1.7" width="100%" height="800" 
    src="https://app.powerbi.com/reportEmbed?reportId=45a8812a-04fe-41ed-b971-b21aca1570cc&autoAuth=true&ctid=6956cdca-e442-489f-b791-39f5bd690f49" 
    frameborder="0" allowFullScreen="true"></iframe>
    """
    
    # Renderiza o HTML do Power BI
    st.components.v1.html(power_bi_code, height=800)
    
    # Botão de Logout (Sair)
    if st.button("Sair"):
        st.session_state["password_correct"] = False
        st.rerun()