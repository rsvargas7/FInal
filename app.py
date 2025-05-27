import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.client as paho
import json

# Configuración de página
st.set_page_config(
    page_title="Plataforma de Comando Vocal",
    page_icon="🎤",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        max-width: 800px;
    }
    .gif-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    .stButton>button {
        height: 60px;
        width: 100%;
        font-size: 18px !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def on_publish(client, userdata, result):
    st.toast("Comando enviado con éxito", icon="✅")

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("voice_control")
client1.on_publish = on_publish

# Diseño mejorado
st.title("🎤 Control por Comando Vocal")
st.markdown("---")

# GIF animado grande (reemplaza con tu URL)
st.markdown('<div class="gif-container">', unsafe_allow_html=True)
st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExc29xcTZvdjZtYXZ3ZXg4MGpwbzM4aTdpMHNlZGtpeDk5bXBmODkzayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UCkZPALajEs8M/giphy.gif",
         use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sección de control por voz
st.markdown("### Presiona el botón y habla:")
st.caption("El sistema reconocerá tu voz y enviará el comando")

stt_button = Button(label=" 🎤 PULSA PARA HABLAR ", 
                  width=300, 
                  height=60,
                  button_type="success",
                  css_classes=["custom-button"])

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

if result and "GET_TEXT" in result:
    client1.connect(broker, port)  
    message = json.dumps({"gesto": result.get("GET_TEXT").strip()})
    client1.publish("Ciaccona", message)
    st.success(f"Comando enviado: '{result.get('GET_TEXT')}'")
    st.balloons()

# Pie de página
st.markdown("---")
st.caption("Sistema de control por voz | Conexión MQTT: broker.mqttdashboard.com:1883")
