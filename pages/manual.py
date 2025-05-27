import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de la página
st.set_page_config(
    page_title="MQTT Control Panel",
    page_icon="🔌",
    layout="wide"
)

# Muestra la versión de Python
st.sidebar.markdown(f"**Versión de Python:** `{platform.python_version()}`")

act1 = "Close"

def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.session_state.last_message = message_received

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Diseño de la interfaz - Versión sin streamlit-extras
st.title("🔌 Panel de Control MQTT")
st.markdown("**Control remoto por protocolo MQTT**")
st.markdown("---")

# Sección de control de actuadores y GIF
col1, col2 = st.columns(2)

with col1:
    st.subheader("Control de Actuadores")
    with st.container(border=True):
        if st.button('🟢 Abrir', key='open_btn', use_container_width=True):
            act1 = "Open"
            client1 = paho.Client("GIT-HUB")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"gesto": act1})
            ret = client1.publish("Ciaccona", message)
            st.toast("Comando 'Abrir' enviado!", icon="🟢")

        if st.button('🔴 Cerrar', key='close_btn', use_container_width=True):
            act1 = "Close"
            client1 = paho.Client("GIT-HUB")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"gesto": act1})
            ret = client1.publish("Ciaccona", message)
            st.toast("Comando 'Cerrar' enviado!", icon="🔴")

with col2:
    with st.container(border=True, height=300): 
        st.subheader("📊 Visualización del Sistema")
        # GIF animado con parámetro actualizado
        st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExam9mdzNocng2Mmc1MGc2dGk5ejlrMzY0NTJ6d2l0M3Nid2Mxdm5jbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/slVWEctHZKvWU/giphy.gif",
            caption="Simulación del sistema en tiempo real",
            use_container_width=True

st.markdown("---")
st.subheader("📨 Mensajes Recibidos")
if 'last_message' not in st.session_state:
    st.session_state.last_message = "Esperando mensajes..."

with st.container(border=True, height=150):
    st.code(st.session_state.last_message, language="json")

st.markdown("---")
st.caption("Conexión MQTT: broker.mqttdashboard.com:1883")
st.caption("Tópico: Ciaccona")
