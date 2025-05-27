import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.client as paho
import json

# Configuración de página
st.set_page_config(
    page_title="Control por Voz Avanzado",
    page_icon="🎙️",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .header {
        text-align: center;
        padding: 15px 0;
    }
    .gif-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        margin: 25px 0;
        border: 1px solid #e0e0e0;
    }
    .voice-button {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white !important;
        font-weight: bold;
        transition: all 0.3s;
    }
    .voice-button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 15px;
        color: #666;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

def on_publish(client, userdata, result):
    st.toast("Comando enviado exitosamente", icon="🚀")

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("voice_control_pro")
client1.on_publish = on_publish

# Encabezado mejorado
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("🎙️ Control por Comando Vocal")
st.markdown("Sistema de reconocimiento de voz integrado con MQTT")
st.markdown('</div>', unsafe_allow_html=True)

# GIF animado grande con parámetro actualizado
st.markdown('<div class="gif-container">', unsafe_allow_html=True)
st.image(
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc25qczhkdXBncHN6aHo2OWxha2R1amZub3RvZ3B1azloYngxOTU3ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/13VBvZfsRkXmCI/giphy.gif",
    use_container_width=True  # Parámetro actualizado
)
st.markdown('</div>', unsafe_allow_html=True)

# Sección de control por voz
st.markdown("### Instrucciones:")
st.markdown("1. Haz clic en el botón de abajo")
st.markdown("2. Habla claramente después del tono")
st.markdown("3. Tu comando se enviará automáticamente")

stt_button = Button(
    label=" 🎤 PULSA PARA HABLAR ", 
    width=300, 
    height=70,
    button_type="success",
    css_classes=["voice-button"]
)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';
 
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
    with st.spinner("Enviando comando..."):
        client1.connect(broker, port)  
        message = json.dumps({"gesto": result.get("GET_TEXT").strip()})
        client1.publish("Ciaccona", message)
        st.success(f"✅ Comando enviado: **'{result.get('GET_TEXT')}'**")
        st.balloons()

# Pie de página mejorado
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("**Sistema de Control por Voz** | v2.0")
st.markdown("Conexión MQTT: `broker.mqttdashboard.com:1883` | Tópico: `Ciaccona`")
st.markdown('</div>', unsafe_allow_html=True)
