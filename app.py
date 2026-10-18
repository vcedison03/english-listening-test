import streamlit as st
import random
import difflib
from io import BytesIO
from gtts import gTTS

# Configuración inicial de la página estilo wide
st.set_page_config(page_title="Práctica de Inglés: Test Dinámico de Estructuras", page_icon="🎓", layout="wide")

# ==========================================
# MOTOR DE GENERACIÓN GRAMATICAL ALEATORIA
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
# BARRA LATERAL DE CONFIGURACIÓN (SIDEBAR)
# ==========================================
st.sidebar.title("Configuración")

nivel = st.sidebar.selectbox(
    "Nivel de exigencia:", 
    ["Flexible (60%)", "Medio (75%)", "Estricto (90%)"], 
    index=2
)

st.sidebar.write("### Modo de cantidad de preguntas:")
modo_preguntas = st.sidebar.radio(
    label="Selecciona una opción:",
    options=["Número específico", "Indefinido (hasta salir)"],
    index=0,
    label_visibility="collapsed"
)

# Inicialización de estados
if 'test_iniciado' not in st.session_state:
    st.session_state.test_iniciado = False
    st.session_state.finalizado = False
    st.session_state.idx = 0
    st.session_state.aciertos = 0
    st.session_state.suma_porcentajes = 0.0
    st.session_state.historial = []
    st.session_state.respondido = False
    st.session_state.oraciones_vistas = set()
    st.session_state.frase_actual = None

if modo_preguntas == "Número específico":
    total_p = st.sidebar.number_input("¿Cuántas oraciones deseas responder?", min_value=1, max_value=50, value=5)
else:
    total_p = 9999

if st.sidebar.button("🔄 Aplicar y Comenzar Test", type="primary"):
    umbrales = {"Flexible (60%)": 60.0, "Medio (75%)": 75.0, "Estricto (90%)": 90.0}
    st.session_state.umbral_exito = umbrales[nivel]
    st.session_state.tipo_exigencia = nivel
    st.session_state.total_preguntas = total_p
    st.session_state.idx = 0
    st.session_state.aciertos = 0
    st.session_state.suma_porcentajes = 0.0
    st.session_state.historial = []
    st.session_state.oraciones_vistas = set()
    st.session_state.frase_actual = generar_frase_aleatoria()
    st.session_state.test_iniciado = True
    st.session_state.finalizado = False
    st.session_state.respondido = False
    st.rerun()

# ==========================================
# INTERFAZ PRINCIPAL DE LA PÁGINA
# ==========================================
st.title("🎓 Práctica de Inglés: Test Interactiva Gramatical")
st.write("Practica tu comprensión auditiva y transcripción con un motor de frases variables infinitas.")

st.info("💡 **Recuerda:** Observa al final de la prueba la retrospectiva y tus audios guardados.")

if not st.session_state.test_iniciado:
    st.warning("👈 Selecciona los parámetros en la barra lateral izquierda y haz clic en **'Aplicar y Comenzar Test'** para iniciar.")

elif st.session_state.finalizado:
    st.success("🎉 ¡Revisión finalizada con éxito!")
    st.write("## ========== RESULTADOS FINALES Y REVISIÓN ==========")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Respondidas", len(st.session_state.historial))
    col2.metric("Aprobadas ✅", st.session_state.aciertos)
    if st.session_state.historial:
        col3.metric("Precisión Promedio 📊", f"{st.session_state.suma_porcentajes / len(st.session_state.historial):.1f}%")
        
    st.write("---")
    for item in st.session_state.historial:
        with st.expander(f"📌 Oración #{item['n']} [{item['tiempo']}] - {item['estado_str']}"):
            st.write(f"**Original (EN):** `{item['oracion']}`")
            st.write(f"**Traducción:** {item['traduccion']}")
            st.write(f"**Tu respuesta:** {item['respuesta']} (*{item['calificacion']:.1f}%*)")
            st.audio(item['audio_bytes'], format="audio/mp3")

else:
    # Evitar desborde del límite específico fijado
    if modo_preguntas == "Número específico" and st.session_state.idx >= total_p:
        st.session_state.finalizado = True
        st.rerun()

    if st.session_state.frase_actual is None:
        nueva_frase = generar_frase_aleatoria()
        intentos = 0
