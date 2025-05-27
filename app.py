import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# Configuración de página
st.set_page_config(
    page_title="Plataforma de Interacción Multicanal",
    page_icon="🗣️",
    layout="wide"
)

def on_publish(client, userdata, result):
    st.toast("Información publicada con éxito", icon="✅")
    print("La información ha sido divulgada\n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    with st.chat_message("assistant"):
        st.write(f"📩 Mensaje recibido: {message_received}")

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("dzukill")
client1.on_message = on_message

# Diseño mejorado
st.title("🗣️ Plataforma de Interacción Multicanal")
st.markdown("---")

# Contenedor principal
with st.container():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Imagen con estilo
        image = Image.open('M.jpg')
        st.image(image, width=200, caption="Sistema de Comando Vocal")
        
        # Botón de voz mejorado
        st.markdown("### 🎤 Comando Vocal")
        st.caption("Presiona el botón para comenzar a hablar")
        
        stt_button = Button(label=" 🎤 INICIAR RECONOCIMIENTO ", 
                          width=300, 
                          height=50,
                          button_type="success")
        
        stt_button.js_on_event("button_click", CustomJS(code="""
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
         
            recognition.onresult = function (e) {
                var value = "";
                for (var i = e.resultIndex; i < e.results.length; ++i) {
                    if (e.results[i].isFinal) {
                        value += e.results[i][0].transcript;
                    }
                }
                if ( value != "") {
                    document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
                }
            }
            recognition.start();
            """))
        
        result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=100,
            debounce_time=0)

    with col2:
        # Área de resultados
        st.markdown("### 📝 Resultados")
        if result:
            if "GET_TEXT" in result:
                with st.chat_message("user"):
                    st.success(f"Texto reconocido: {result.get('GET_TEXT')}")
                
                client1.on_publish = on_publish                            
                client1.connect(broker, port)  
                message = json.dumps({"gesto": result.get("GET_TEXT").strip()})
                ret = client1.publish("Ciaccona", message)
                st.toast("Comando enviado al broker MQTT", icon="📡")

        # Área de mensajes
        st.markdown("### 📨 Mensajes Recibidos")
        if 'message_received' in globals():
            with st.chat_message("assistant"):
                st.info(message_received)

# Configuración adicional
try:
    os.mkdir("temp")
except:
    pass

# Pie de página
st.markdown("---")
st.caption("🔗 Conexión MQTT: broker.mqttdashboard.com:1883 | 📡 Tópico: Ciaccona")
st.caption("Sistema de interacción multicanal - v1.0")
