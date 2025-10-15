import streamlit as st
import pandas as pd
import os
import platform
import subprocess
from streamlit.components.v1 import html
from streamlit_modal import Modal

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Injetoras",
    page_icon="🏭",
    layout="wide"
)

# --- GERENCIAMENTO DE DADOS (CSV) ---
DATA_FILE = "injetoras.csv"

def load_data():
    expected_columns = [
        'tag', 'grupo', 'ip_injetora', 'ip_dosador', 'id_dosador', 'ip_coletor',
        'tag_ont', 'status_opcua', 'observacoes', 'status_geral', 'dependente_syneco'
    ]
    
    # AQUI ESTÁ A CORREÇÃO: Forçamos as colunas a serem do tipo 'str' (texto)
    dtype_mapping = {
        'tag': str,
        'id_dosador': str,
        'tag_ont': str,
        'observacoes': str,
        'dependente_syneco': str
    }

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, dtype=dtype_mapping)
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        return df
    else:
        return pd.DataFrame(columns=expected_columns)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- FUNÇÃO DE PING ---
@st.cache_data(ttl=60)
def check_ping(ip):
    try:
        if pd.isna(ip) or str(ip).strip() == '': return False
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w', '1', str(ip)]
        response = subprocess.run(command, capture_output=True)
        return response.returncode == 0
    except Exception:
        return False

# Dicionário de Ícones
ICONS = {
    "grupo": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-collection-fill' viewBox='0 0 16 16'%3E%3Cpath d='M0 13a1.5 1.5 0 0 0 1.5 1.5h13A1.5 1.5 0 0 0 16 13V6a1.5 1.5 0 0 0-1.5-1.5h-13A1.5 1.5 0 0 0 0 6v7zM2 3a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 0-1h-11A.5.5 0 0 0 2 3zm2-2a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 0-1h-7A.5.5 0 0 0 4 1z'/%3E%3C/svg%3E",
    "status_ok": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='green' class='bi bi-check-circle-fill' viewBox='0 0 16 16'%3E%3Cpath d='M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z'/%3E%3C/svg%3E",
    "status_nok": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='red' class='bi bi-x-circle-fill' viewBox='0 0 16 16'%3E%3Cpath d='M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z'/%3E%3C/svg%3E",
    "status_off": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='gray' class='bi bi-question-circle-fill' viewBox='0 0 16 16'%3E%3Cpath d='M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.454 6.03a.5.5 0 0 0-.707 0l-.708.707a.5.5 0 0 0 0 .708l.707.707a.5.5 0 0 0 .708 0l.707-.707a.5.5 0 0 0 0-.708l-.707-.707zM7 5.111a1.002 1.002 0 0 0-1.414 0l-.707.707a1 1 0 0 0-.293.707V10.5a.5.5 0 0 0 1 0V7.933a1 1 0 0 0 .293-.707l.707-.707A1 1 0 0 0 7 5.111zm2.57 6.345a.5.5 0 0 0-.707 0l-.707.707a.5.5 0 0 0 0 .708l.707.707a.5.5 0 0 0 .708 0l.707-.707a.5.5 0 0 0 0-.708l-.707-.707z'/%3E%3C/svg%3E",
    "ip": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-globe' viewBox='0 0 16 16'%3E%3Cpath d='M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm7.5-6.923c-.67.204-1.335.82-1.887 1.855A7.97 7.97 0 0 0 5.145 4.06a.933.933 0 0 1 1.031-1.262.798.798 0 0 0 .621-.372A8.008 8.008 0 0 1 7.5.077zM4.06 4.851a.7.7 0 0 1 .582 1.141A7.043 7.043 0 0 0 4.043 8a7.043 7.043 0 0 0 .556 2.008.7.7 0 0 1-1.141.582A8.01 8.01 0 0 1 3 8c0-.66.1-1.3.28-1.897.143-.486.335-.958.58-1.392zM8.5 4.06a.933.933 0 0 1 1.262 1.031A7.97 7.97 0 0 0 10.855 8a7.97 7.97 0 0 0-.001 2.909.933.933 0 0 1-1.262 1.031.798.798 0 0 0-.621-.372A8.008 8.008 0 0 1 8.5 4.06zm-1-2.986A8.008 8.008 0 0 0 7.378 2.44a.798.798 0 0 0 .622.372.933.933 0 0 1 1.03 1.262A7.97 7.97 0 0 0 9.855 8a7.97 7.97 0 0 0 .001 2.909.933.933 0 0 1-1.03 1.262.798.798 0 0 0-.622.372A8.008 8.008 0 0 0 8.5 11.94c.67-.204 1.335-.82 1.887-1.855.552-1.035.8-2.13.8-3.085s-.248-2.05-.8-3.085c-.552-1.035-1.217-1.651-1.887-1.855z'/%3E%3C/svg%3E",
    "ont": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-ethernet' viewBox='0 0 16 16'%3E%3Cpath d='M1.525 5.025a.5.5 0 0 1 .434.743L1.243 7H2.5a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H1.243l.716 1.232a.5.5 0 0 1-.868.506L.025 8.5H.5a.5.5 0 0 1 0-1H.025l1.066-1.83a.5.5 0 0 1 .434-.245zM4.5 1.5A1.5 1.5 0 0 1 6 0h4a1.5 1.5 0 0 1 1.5 1.5v13A1.5 1.5 0 0 1 10 16H6a1.5 1.5 0 0 1-1.5-1.5v-13zM6 2h4a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H6a.5.5 0 0 1-.5-.5v-1A.5.5 0 0 1 6 2zm0 12h4a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H6a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zM14.475 5.025a.5.5 0 0 1 .434.245L15.975 7H16a.5.5 0 0 1 0 1h-.025l-1.066 1.83a.5.5 0 0 1-.868-.506l.716-1.232H13.5a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h1.257l-.716-1.232a.5.5 0 0 1 .434-.743z'/%3E%3C/svg%3E",
    "obs": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-pencil-square' viewBox='0 0 16 16'%3E%3Cpath d='M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z'/%3E%3Cpath fill-rule='evenodd' d='M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z'/%3E%3C/svg%3E",
    "id_card": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-person-vcard' viewBox='0 0 16 16'%3E%3Cpath d='M5 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm4-2.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5ZM9 8a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4A.5.5 0 0 1 9 8Zm1 2.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5Z'/%3E%3Cpath d='M2 2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H2ZM1 4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H8.96c.026-.163.04-.33.04-.5C9 10.567 7.21 9 5 9c-2.086 0-3.8 1.398-3.984 3.181A1.006 1.006 0 0 1 1 12V4Z'/%3E%3C/svg%3E",
    "dependency": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-link-45deg' viewBox='0 0 16 16'%3E%3Cpath d='M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z'/%3E%3Cpath d='M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243L6.586 4.672z'/%3E%3C/svg%3E"
}

# --- Barra Lateral e Navegação ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma página", ["Dashboard Geral", "Mapa de Cartões", "Gerenciar Equipamentos"])
st.title(f"🏭 {page}")
st.markdown("---")

# --- Lógica e Exibição das Páginas ---
df = load_data()

if page == "Dashboard Geral":
    def style_status_geral(row):
        color = '#D4EDDA' if row.status_geral == 'OK' else ''
        return [f'background-color: {color}'] * len(row)

    if st.button("📡 Verificar Conectividade de Rede (Ping)"):
        all_ips = pd.concat([df['ip_injetora'], df['ip_dosador'], df['ip_coletor']]).dropna().unique()
        progress_bar = st.progress(0, text="Pinging equipamentos...")
        ping_results = {}
        for i, ip in enumerate(all_ips):
            ping_results[ip] = check_ping(ip)
            progress_bar.progress((i + 1) / len(all_ips), text=f"Pinging {ip}...")
        st.session_state.ping_results = ping_results
        progress_bar.empty()
        st.success("Verificação de ping concluída!")

    search_query = st.text_input("🔎 Pesquisar por TAG, IP, Grupo ou Observação")
    df_filtrado = df
    if search_query:
        search_query = search_query.lower()
        mask = df.apply(lambda row: any(search_query in str(val).lower() for val in row), axis=1)
        df_filtrado = df[mask]

    st.header("Visão Geral do Status")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Injetoras", f"{len(df)}")
    col2.metric("Status Geral OK", f"{len(df[df['status_geral'] == 'OK'])}")
    col3.metric("Status Geral Não OK", f"{len(df[df['status_geral'] == 'Não OK'])}")
    
    df_display = df_filtrado.copy()
    if 'ping_results' in st.session_state:
        df_display['Ping Injetora'] = df_display['ip_injetora'].apply(lambda ip: '🟢' if st.session_state.ping_results.get(ip) else ('🔴' if pd.notna(ip) and ip in st.session_state.ping_results else '⚪'))
        df_display['Ping Dosador'] = df_display['ip_dosador'].apply(lambda ip: '🟢' if st.session_state.ping_results.get(ip) else ('🔴' if pd.notna(ip) and ip in st.session_state.ping_results else '⚪'))
        df_display['Ping Coletor'] = df_display['ip_coletor'].apply(lambda ip: '🟢' if st.session_state.ping_results.get(ip) else ('🔴' if pd.notna(ip) and ip in st.session_state.ping_results else '⚪'))
    
    st.dataframe(df_display.style.apply(style_status_geral, axis=1), use_container_width=True)
    st.caption("Status do Ping: 🟢 Online | 🔴 Offline | ⚪ Não Testado")

elif page == "Mapa de Cartões":
    modal = Modal(key="details-modal", title="Detalhes do Equipamento")
    if df.empty:
        st.warning("Nenhuma injetora cadastrada.")
    else:
        grupos = ['Todos'] + sorted(df['grupo'].astype(str).unique().tolist())
        grupo_selecionado = st.selectbox("Selecione um Anexo para visualizar:", grupos)
        df_filtrado = df if grupo_selecionado == 'Todos' else df[df['grupo'] == grupo_selecionado]
        
        status_geral_icon_map = {"OK": ICONS["status_ok"], "Não OK": ICONS["status_nok"]}
        status_opcua_icon_map = {"Conectado": ICONS["status_ok"], "Não Conectado": ICONS["status_nok"], "Sem OPCUA": ICONS["status_off"]}
        
        COLUMNS = 4
        cols = st.columns(COLUMNS)
        for i, row in df_filtrado.iterrows():
            col_index = i % COLUMNS
            with cols[col_index]:
                with st.container():
                    status_geral_icon = status_geral_icon_map.get(row['status_geral'], ICONS["status_off"])
                    card_color = '#D4EDDA' if row.status_geral == 'OK' else '#FFFFFF'
                    
                    card_html = f"""
                    <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.04); height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background-color: {card_color};">
                        <h3 style="margin: 0 0 10px 0; font-size: 1.5em;">Injetora {row['tag']}</h3>
                        <div style="display: flex; align-items: center; font-size: 1.1em;">
                            <img src="{status_geral_icon}" style="width: 18px; height: 18px; margin-right: 8px;">
                            <span>{row.get('status_geral') or 'Não definido'}</span>
                        </div>
                    </div>
                    """
                    html(card_html, height=125)
                    if st.button("Ver Detalhes", key=f"btn_{row['tag']}", use_container_width=True):
                        st.session_state.selected_injetora = row
                        modal.open()
    
    if modal.is_open() and 'selected_injetora' in st.session_state:
        with modal.container():
            data = st.session_state.selected_injetora.to_dict()
            status_opcua_icon = status_opcua_icon_map.get(data['status_opcua'])
            
            modal_content_html = f"""
            <style>
                .modal-body h2 {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; }} .modal-body .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }} .modal-body .info-item {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; }} .modal-body .info-item strong {{ display: flex; align-items: center; }} .modal-body .info-item img {{ width: 16px; height: 16px; margin-right: 8px; }} .modal-body .full-width {{ grid-column: 1 / -1; }} .modal-body code {{ background-color: #e9ecef; padding: 2px 4px; border-radius: 3px; }}
            </style>
            <div class="modal-body">
                <h2>Injetora {data['tag']}</h2>
                <div class="info-grid">
                    <div class="info-item"><strong><img src="{ICONS['grupo']}">Anexo:</strong> {data['grupo']}</div>
                    <div class="info-item"><strong><img src="{status_opcua_icon}">Status OPCUA:</strong> {data['status_opcua']}</div>
                    <div class="info-item"><strong><img src="{status_geral_icon_map.get(data['status_geral'], ICONS['status_off'])}">Status Geral:</strong> {data.get('status_geral') or 'N/A'}</div>
                    <div class="info-item"><strong><img src="{ICONS['dependency']}">Dependente Syneco:</strong> {data.get('dependente_syneco') or 'Nenhum'}</div>
                    <div class="info-item"><strong><img src="{ICONS['ip']}">IP Injetora:</strong> <code>{data.get('ip_injetora') or 'N/A'}</code></div>
                    <div class="info-item"><strong><img src="{ICONS['ip']}">IP Dosador Motan:</strong> <code>{data.get('ip_dosador') or 'N/A'}</code></div>
                    <div class="info-item"><strong><img src="{ICONS['id_card']}">ID do Dosador Motan:</strong> <code>{data.get('id_dosador') or 'N/A'}</code></div>
                    <div class="info-item"><strong><img src="{ICONS['ip']}">IP Syneco:</strong> <code>{data.get('ip_coletor') or 'N/A'}</code></div>
                    <div class="info-item full-width"><strong><img src="{ICONS['ont']}">ID da ONT:</strong> <code>{data.get('tag_ont') or 'N/A'}</code></div>
                    <div class="info-item full-width">
                        <strong><img src="{ICONS['obs']}">Observações:</strong> <p>{data.get('observacoes') or 'Nenhuma'}</p>
                    </div>
                </div>
            </div>
            """
            html(modal_content_html, height=500, scrolling=True)

elif page == "Gerenciar Equipamentos":
    st.header("Gerenciar Injetoras")
    st.info("Para adicionar, editar ou remover, use a tabela interativa abaixo. Clique em 'Salvar Alterações' para persistir as mudanças no arquivo.")

    tag_options = ["Nenhum"] + [tag for tag in df['tag'].astype(str).unique() if tag and pd.notna(tag)]

    edited_df = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "grupo": st.column_config.SelectboxColumn("Anexo", options=["A3", "A4", "A5"], required=True),
            "status_opcua": st.column_config.SelectboxColumn("Status OPCUA", options=["Conectado", "Não Conectado", "Sem OPCUA"], required=True),
            "status_geral": st.column_config.SelectboxColumn("Status Geral", options=["OK", "Não OK"], required=False),
            "dependente_syneco": st.column_config.SelectboxColumn("Dependente Syneco", options=tag_options, required=False),
            "tag": st.column_config.TextColumn("ID da Injetora (TAG)", required=True),
            "ip_injetora": "IP da Injetora",
            "ip_dosador": "IP Dosador Motan",
            "id_dosador": "ID Dosador Motan",
            "ip_coletor": "IP Syneco",
            "tag_ont": st.column_config.TextColumn("ID da ONT"),
            "observacoes": st.column_config.TextColumn("Observações")
        },
        key="injetoras_editor"
    )

    if st.button("Salvar Alterações", type="primary"):
        edited_df['tag'] = edited_df['tag'].astype(str)
        
        if edited_df['tag'].str.strip().eq('').any():
             st.error("Erro: O 'ID da Injetora (TAG)' não pode ser vazio. Por favor, preencha todas as TAGs.")
        elif edited_df['tag'].duplicated().any():
            st.error("Erro: Existem 'IDs da Injetora' duplicados. Por favor, corrija antes de salvar.")
        else:
            save_data(edited_df)
            st.success("Alterações salvas com sucesso!")
            st.rerun()
