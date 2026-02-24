import streamlit as st
import requests
import json
import boto3
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Amazon Financial Agent", page_icon="📈", layout="wide")
load_dotenv()

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; }
    .tool-box { background-color: #1e2130; border-left: 5px solid #00ffa2; padding: 10px; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Amazon Financial Agent")
st.subheader("Análisis de Grado Empresarial con Claude 3.5 & AWS")

def get_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'), msg=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

with st.sidebar:
    st.header("🔑 Autenticación")
    email = st.text_input("Email", value="test_user@example.com")
    password = st.text_input("Contraseña", type="password", value="YourPassword123!")
    login_btn = st.button("Iniciar Sesión")

    if login_btn:
        try:
            client = boto3.client('cognito-idp', region_name=os.getenv("AWS_REGION", "us-east-2"))
            s_hash = get_secret_hash(email, os.getenv("CLIENT_ID"), os.getenv("COGNITO_CLIENT_SECRET"))
            
            resp = client.initiate_auth(
                ClientId=os.getenv("CLIENT_ID"),
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={'USERNAME': email, 'PASSWORD': password, 'SECRET_HASH': s_hash}
            )
            st.session_state.token = resp['AuthenticationResult']['AccessToken']
            st.success("Conectado a AWS Cognito")
        except Exception as e:
            st.error(f"Error: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pregunta sobre Amazon (Ej: Precio actual o Q4 2024)"):
    if "token" not in st.session_state:
        st.warning("⚠️ Por favor, inicia sesión primero.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            
            try:
                with requests.post("http://localhost:8000/chat", json={"message": prompt}, headers=headers, stream=True) as r:
                    for line in r.iter_lines():
                        if line:
                            chunk = line.decode('utf-8').replace("data: ", "")
                            try:
                                data = json.loads(chunk)
                                
                                if "agent" in data:
                                    msg = data["agent"]["messages"][-1]
                                    if isinstance(msg, str):
                                        full_response += msg + " "
                                    elif isinstance(msg, list):
                                        for m in msg:
                                            if m.get('type') == 'text':
                                                st.caption(f"🧠 *Pensando: {m['text']}*")
                                            if m.get('type') == 'tool_use':
                                                st.info(f"🛠️ **Usando herramienta:** {m['name']}")
                                
                                elif "tools" in data:
                                    st.success(f"📊 **Resultado:** {data['tools']['messages'][0]}")
                                
                                response_placeholder.markdown(full_response + "▌")
                            except:
                                continue
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Fallo de conexión: {e}")
