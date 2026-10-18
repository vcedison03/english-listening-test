import streamlit as st
import random
import difflib
from io import BytesIO
from gtts import gTTS

# Configuración inicial de la página
st.set_page_config(page_title="Test de Listening Avanzado", page_icon="🎧", layout="centered")

# ==========================================
# BANCO DE VOCABULARIO EXPANDIDO
# ==========================================
sujetos = ["The teacher", "A student", "My friend", "The chef", "An artist", "Our neighbor", "The doctor", "A mechanic"]
verbos_presente = [("drinks", "toma"), ("prepares", "prepara"), ("reads", "lee"), ("paints", "pinta"), ("cleans", "limpia")]
verbos_futuro = [("visit", "visitará"), ("build", "construirá"), ("buy", "comprará"), ("learn", "aprenderá"), ("organize", "organizará")]
verbos_pasado = [("drank", "tomó"), ("prepared", "preparó"), ("read", "leyó"), ("painted", "pintó"), ("cleaned", "limpió")]
verbos_participio = [("drunk", "tomado"), ("prepared", "preparado"), ("read", "leído"), ("painted", "pintado"), ("cleaned", "limpiado")]
verbos_infinitivo = [("drink", "tomar"), ("prepare", "preparar"), ("read", "leer"), ("paint", "pintar"), ("clean", "limpiar")]

objetos = [("coffee", "café"), ("a book", "un libro"), ("a house", "una casa"), ("a car", "un carro"), ("a project", "un proyecto")]
lugares = [("in the morning", "por la mañana"), ("at home", "en casa"), ("in the office", "en la oficina"), ("every day", "todos los días")]

condiciones_presente = [("it rains", "llueve"), ("you study", "estudias"), ("they practice", "practican")]
condiciones_pasado = [("it rained", "llovía"), ("you studied", "estudiaste"), ("they practiced", "practicaron")]
condiciones_perfectas = [("it had rained", "hubiera llovido"), ("you had studied", "hubieras estudiado")]

def generar_frase_aleatoria():
    tiempos_disponibles = [
        "Presente Simple", "Futuro Simple", "Presente Continuo", 
        "Pasado Simple", "Pasado Continuo", "Presente Perfecto", "Voz Pasiva",
        "Modales Básicos", "Modales Avanzados", 
        "Condicional Cero", "Primer Condicional", "Segundo Condicional", "Tercer Condicional"
    ]
    tiempo_tipo = random.choice(tiempos_disponibles)
    sujeto = random.choice(sujetos)
    obj_en, obj_es = random.choice(objetos)
    lugar_en, lugar_es = random.choice(lugares)
    
    if tiempo_tipo == "Presente Simple":
        verbo_en, verbo_es = random.choice(verbos_presente)
        en = f"{sujeto} {verbo_en} {obj_en} {lugar_en}."
        es = f"{sujeto} {verbo_es} {obj_es} {lugar_es}."
    elif tiempo_tipo == "Futuro Simple":
        verbo_en, verbo_es = random.choice(verbos_futuro)
        en = f"{sujeto} will {verbo_en} {obj_en} tomorrow."
        es = f"{sujeto} {verbo_es} {obj_es} mañana."
    elif tiempo_tipo == "Presente Continuo":
        verbo_en, verbo_es = random.choice([("working on", "trabajando en"), ("studying", "estudiando")])
        en = f"{sujeto} is {verbo_en} {obj_en} right now."
        es = f"{sujeto} está {verbo_es} {obj_es} ahora mismo."
    elif tiempo_tipo == "Pasado Simple":
        verbo_en, verbo_es = random.choice(verbos_pasado)
        en = f"{sujeto} {verbo_en} {obj_en} yesterday."
        es = f"{sujeto} {verbo_es} {obj_es} ayer."
    elif tiempo_tipo == "Pasado Continuo":
        verbo_en, verbo_es = random.choice([("preparing", "preparando"), ("reading", "leyendo"), ("cleaning", "limpiando")])
        en = f"{sujeto} was {verbo_en} {obj_en} when I arrived."
        es = f"{sujeto} estaba {verbo_es} {obj_es} cuando llegué."
    elif tiempo_tipo == "Presente Perfecto":
        verbo_en, verbo_es = random.choice(verbos_participio)
        en = f"{sujeto} has {verbo_en} {obj_en} recently."
        es = f"{sujeto} ha {verbo_es} {obj_es} recientemente."
    elif tiempo_tipo == "Voz Pasiva":
        verbo_en, verbo_es = random.choice(verbos_participio)
        en = f"{obj_en.capitalize()} was {verbo_en} by {sujeto.lower()}."
        es = f"{obj_es.capitalize()} fue {verbo_es} por {sujeto.lower()}."
    elif tiempo_tipo == "Modales Básicos":
        modal = random.choice([("should", "debería"), ("can", "puede"), ("must", "debe")])
        verbo_en, verbo_es = random.choice(verbos_infinitivo)
        en = f"{sujeto} {modal} {verbo_en} {obj_en}."
        es = f"{sujeto} {modal} {verbo_en} {obj_es}."
    elif tiempo_tipo == "Modales Avanzados":
        modal = random.choice([("ought to", "debería"), ("would", "gustaría"), ("might", "podría")])
        verbo_en, verbo_es = random.choice(verbos_infinitivo)
        if modal == "would":
            en = f"{sujeto} {modal} {verbo_en} {obj_en}."
            es = f"A {sujeto.lower()} le {verbo_es[:-2]}aría {obj_es}."
        else:
            en = f"{sujeto} {modal} {verbo_en} {obj_en}."
            es = f"{sujeto} {modal} {verbo_en} {obj_es}."
    elif tiempo_tipo == "Condicional Cero":
        cond_en, cond_es = random.choice(condiciones_presente)
        verbo_en, verbo_es = random.choice(verbos_presente)
        en = f"If {cond_en}, {sujeto.lower()} {verbo_en} {obj_en}."
        es = f"Si {cond_es}, {sujeto.lower()} {verbo_es} {obj_es}."
    elif tiempo_tipo == "Primer Condicional":
        cond_en, cond_es = random.choice(condiciones_presente)
        verbo_en, verbo_es = random.choice(verbos_futuro)
        en = f"If {cond_en}, {sujeto.lower()} will {verbos_infinitivo[verbos_futuro.index((verbo_en, verbo_es))]} {obj_en}."
        es = f"Si {cond_es}, {sujeto.lower()} {verbo_es} {obj_es}."
    elif tiempo_tipo == "Segundo Condicional":
        cond_en, cond_es = random.choice(condiciones_pasado)
        verbo_en, verbo_es = random.choice(verbos_infinitivo)
        en = f"If {cond_en}, {sujeto.lower()} would {verbo_en} {obj_en}."
        es = f"Si {cond_es}, {sujeto.lower()} le {verbo_es[:-2]}aría {obj_en}."
    else:
        cond_en, cond_es = random.choice(condiciones_perfectas)
        verbo_en, verbo_es = random.choice(verbos_participio)
        en = f"If {cond_en}, {sujeto.lower()} would have {verbo_en} {obj_en}."
        es = f"Si {cond_es}, {sujeto.lower()} habría {verbo_es} {obj_es}."

    return {"tiempo": tiempo_tipo, "en": en, "es": es}

def generar_audio_bytes(texto):
    tts = gTTS(text=texto, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ==========================================
# GESTIÓN DEL ESTADO DE STREAMLIT
# ==========================================
if 'configurado' not in st.session_state:
    st.session_state.configurado = False
    st.session_state.finalizado = False
    st.session_state.idx = 0
    st.session_state.aciertos = 0
    st.session_state.suma_porcentajes = 0.0
    st.session_state.historial = []
    st.session_state.oraciones_sesion = []
    st.session_state.respondido = False
    st.session_state.resultado_actual = {}

# --- PANTALLA 1: CONFIGURACIÓN ---
if not st.session_state.configurado:
    st.title("🎧 Test de Listening Interactiva")
    st.subheader("Configura tu sesión de práctica")
    
    total_p = st.number_input("Número de preguntas:", min_value=1, max_value=20, value=5)
    nivel = st.selectbox("Nivel de exigencia:", ["Flexible (60%)", "Medio (75%)", "Estricto (90%)"], index=1)
    
    if st.button("🚀 Iniciar Test", type="primary"):
        umbrales = {"Flexible (60%)": 60.0, "Medio (75%)": 75.0, "Estricto (90%)": 90.0}
        st.session_state.umbral_exito = umbrales[nivel]
        st.session_state.tipo_exigencia = nivel
        st.session_state.total_preguntas = total_p
        st.session_state.oraciones_sesion = [generar_frase_aleatoria() for _ in range(total_p)]
        st.session_state.configurado = True
        st.rerun()

# --- PANTALLA 3: RESULTADOS FINALES ---
elif st.session_state.finalizado:
    st.title("🏁 Resultados Finales y Revisión")
    st.metric(label="⚙️ Nivel", value=st.session_state.tipo_exigencia)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Respondidas", len(st.session_state.historial))
    col2.metric("Aprobadas ✅", st.session_state.aciertos)
    if len(st.session_state.historial) > 0:
        col3.metric("Precisión Promedio 📊", f"{st.session_state.suma_porcentajes / len(st.session_state.historial):.1f}%")

    st.write("---")
    st.subheader("📋 Historial de Oraciones Practicadas")
    
    for item in st.session_state.historial:
        with st.expander(f"📌 {item['n']}. [{item['tiempo']}] - {item['estado_str']}"):
            st.write(f"**Original (EN):** `{item['oracion']}`")
            st.write(f"**Traducción (ES):** {item['traduccion']}")
            st.write(f"**Tu respuesta:** {item['respuesta']} (*{item['calificacion']:.1f}%*)")
            st.audio(item['audio_bytes'], format="audio/mp3")

    if st.button("🔄 Reiniciar nuevo test"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- PANTALLA 2: JUEGO / PREGUNTAS ---
else:
    if st.session_state.idx >= len(st.session_state.oraciones_sesion):
        st.session_state.finalizado = True
        st.rerun()
        
    frase_actual = st.session_state.oraciones_sesion[st.session_state.idx]
    
    st.title(f"Pregunta {st.session_state.idx + 1} de {st.session_state.total_questions if 'total_questions' in st.session_state else st.session_state.total_preguntas}")
    st.info(f"💡 Estructura gramatical: **{frase_actual['tiempo']}**")
    
    # Generar audio
    audio_bytes = generar_audio_bytes(frase_actual['en'])
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    
    # Formulario de respuesta
    with st.form(key=f"form_{st.session_state.idx}"):
        respuesta_usuario = st.text_input("Escribe exactamente lo que escuchaste en inglés:", key=f"input_{st.session_state.idx}").strip()
        submit_btn = st.form_submit_with_colorkey = st.form_submit_button("Calificar 🔍", type="primary")
        
    if submit_btn:
        if not respuesta_usuario:
            st.warning("⚠️ Por favor escribe una respuesta antes de calificar.")
        else:
