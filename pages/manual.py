import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de la página
st.set_page_config(
    page_title="Flor",
    page_icon="🌼",
    layout="wide"
)

# Muestra la versión de Python
st.sidebar.markdown(f"**Versión de Python:** `{platform.python_version()}`")

act1 = "close"

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

# Diseño de la interfaz mejorado
st.title("🏵️ Boton de OPEN y CLOSE 🏵️")
st.markdown("**Funcion de botones de Open y Close para tu flor y un Pikachu parchado al lado**")
st.markdown("---")

# Sección principal con dos columnas
col1, col2 = st.columns([1, 1.2])  # Ajuste de proporciones

with col1:
    with st.container(border=True):
        st.subheader("🛠️ Control de Actuadores")
        
        btn_open = st.button('🟢 ABRIR', key='open_btn', 
                           use_container_width=True,
                           help="Enviar comando de apertura")
        
        if btn_open:
            act1 = "Open"
            client1 = paho.Client("GIT-HUB")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"gesto": act1})
            client1.publish("Ciaccona", message)
            st.toast("Comando 'Abrir' enviado!", icon="🟢")

        btn_close = st.button('🔴 CERRAR', key='close_btn',
                            use_container_width=True,
                            help="Enviar comando de cierre")
        
        if btn_close:
            act1 = "Close"
            client1 = paho.Client("GIT-HUB")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"gesto": act1})
            client1.publish("Ciaccona", message)
            st.toast("Comando 'Cerrar' enviado!", icon="🔴")

with col2:
    with st.container(border=True, height=300):  # Altura fija para mejor alineación
        st.subheader("⚡ Pikachu tomando ronsito ⚡")
        
        # GIF animado con parámetro actualizado
        st.image(
            "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExam9mdzNocng2Mmc1MGc2dGk5ejlrMzY0NTJ6d2l0M3Nid2Mxdm5jbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/slVWEctHZKvWU/giphy.gif",
            caption="Simulación del sistema en tiempo real",
            use_container_width=True  # Parámetro actualizado
        )

# Pie de página
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.caption("🌐 **Conexión MQTT:** broker.mqttdashboard.com:1883")
with footer_col2:
    st.caption("📡 **Tópico:** Ciaccona")
