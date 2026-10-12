from io import BytesIO
import random
from difflib import SequenceMatcher
from gtts import gTTS
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Practice of English Tenses", page_icon="🎧", layout="centered"
)

st.title("🎧 Practice of English Tenses")
st.write(
    "Escucha el audio generado y escribe exactamente la frase en inglés que escuchas."
)

# Banco de vocabulario por categorías
sujetos = [
    "The teacher",
    "A student",
    "My friend",
    "The chef",
    "An artist",
    "Our neighbor",
    "The doctor",
    "A mechanic",
]
verbos_presente = [
    ("drinks", "toma"),
    ("prepares", "prepara"),
    ("reads", "lee"),
    ("paints", "pinta"),
    ("cleans", "limpia"),
]
verbos_futuro = [
    ("visit", "visitará"),
    ("build", "construirá"),
    ("buy", "comprará"),
    ("learn", "aprenderá"),
    ("organize", "organizará"),
]
objetos = [
    ("coffee", "café"),
    ("a book", "un libro"),
    ("a house", "una casa"),
    ("a car", "un carro"),
    ("a project", "un proyecto"),
]
lugares = [
    ("in the morning", "por la mañana"),
    ("at home", "en casa"),
    ("in the office", "en la oficina"),
    ("every day", "todos los días"),
]


def generar_todas_las_frases():
    """Genera un banco completo de frases posibles para evitar duplicados."""
    todas = []
    
    # Presente Simple
    for sujeto in sujetos:
        for verbo_en, verbo_es in verbos_presente:
            for obj_en, obj_es in objetos:
                for lugar_en, lugar_es in lugares:
                    todas.append({
                        "tiempo": "Presente Simple",
                        "en": f"{sujeto} {verbo_en} {obj_en} {lugar_en}.",
                        "es": f"{sujeto} {verbo_es} {obj_es} {lugar_es}."
                    })

    # Futuro Simple
    for sujeto in sujetos:
        for verbo_en, verbo_es in verbos_futuro:
            for obj_en, obj_es in objetos:
                todas.append({
                    "tiempo": "Futuro Simple",
                    "en": f"{sujeto} will {verbo_en} {obj_en} tomorrow.",
                    "es": f"{sujeto} {verbo_es} {obj_es} mañana."
                })

    # Presente Continuo
    for sujeto in sujetos:
        for verbo_en, verbo_es in [("working on", "trabajando en"), ("studying", "estudiando")]:
            for obj_en, obj_es in objetos:
                todas.append({
                    "tiempo": "Presente Continuo",
                    "en": f"{sujeto} is {verbo_en} {obj_en} right now.",
                    "es": f"{sujeto} está {verbo_es} {obj_es} ahora mismo."
                })
                
    return todas


# Inicializar el estado de la sesión
if "configurado" not in st.session_state:
    st.session_state.configurado = False
    st.session_state.paso = 0
    st.session_state.puntuacion = 0
    st.session_state.respondido = False
    st.session_state.resultado_ultimo = None
    st.session_state.preguntas_test = []
    st.session_state.tolerancia_elegida = 0.85

# Pantalla de configuración inicial (antes de empezar)
if not st.session_state.configurado:
    st.subheader("⚙️ Configuración del Test")
    
    # Calcular el máximo posible de frases únicas
    banco_temporal = generar_todas_las_frases()
    max_preguntas = len(banco_temporal)
    
    total_elegido = st.slider(
        "¿Cuántas preguntas deseas en este test?",
        min_value=3,
        max_value=min(20, max_preguntas),
        value=5
    )

    # Selector para el nivel de exigencia / tolerancia
    modo_exigencia = st.select_slider(
        "Nivel de exigencia en la calificación:",
        options=["Muy flexible (70%)", "Flexible (80%)", "Normal (85%)", "Estricto (95%)", "Exacto (100%)"],
        value="Normal (85%)"
    )

    # Mapear la opción seleccionada a un valor decimal
    mapeo_tolerancia = {
        "Muy flexible (70%)": 0.70,
        "Flexible (80%)": 0.80,
        "Normal (85%)": 0.85,
        "Estricto (95%)": 0.95,
        "Exacto (100%)": 1.00
    }
    
    if st.button("🚀 Comenzar Test"):
        st.session_state.preguntas_test = random.sample(banco_temporal, total_elegido)
        st.session_state.tolerancia_elegida = mapeo_tolerancia[modo_exigencia]
        st.session_state.configurado = True
        st.session_state.paso = 0
        st.session_state.puntuacion = 0
        st.rerun()

else:
    total_preguntas = len(st.session_state.preguntas_test)

    # Si la prueba no ha terminado
    if st.session_state.paso < total_preguntas:
        ej_actual = st.session_state.preguntas_test[st.session_state.paso]
        
        st.subheader(
            f"Pregunta {st.session_state.paso + 1} de {total_preguntas}"
        )
        st.info(f"Tiempo verbal: **{ej_actual['tiempo']}**")

        # Generar o recuperar el audio guardado en la sesión
        if "audio_bytes" not in st.session_state or st.session_state.get("paso_audio") != st.session_state.paso:
            tts = gTTS(text=ej_actual["en"], lang="en")
            fp = BytesIO()
            tts.write_to_fp(fp)
            st.session_state.audio_bytes = fp.getvalue()
            st.session_state.paso_audio = st.session_state.paso

        st.audio(st.session_state.audio_bytes, format="audio/mp3")

        # Formulario de respuesta
        with st.form(key=f"form_{st.session_state.paso}"):
            respuesta = st.text_input(
                "Escribe lo que escuchaste en inglés:", key=f"input_{st.session_state.paso}"
            )
            submit_button = st.form_submit_button(label="Enviar respuesta")

            if submit_button:
                limpia_original = ej_actual["en"].rstrip("?.!").lower()
                limpia_respuesta = respuesta.rstrip("?.!").lower()

                # Calificación basada en la tolerancia elegida por el usuario
                similitud = SequenceMatcher(None, limpia_respuesta, limpia_original).ratio()

                st.session_state.respondido = True
                if similitud >= st.session_state.tolerancia_elegida:
                    st.session_state.puntuacion += 1
                    st.session_state.resultado_ultimo = "correcto"
                else:
                    st.session_state.resultado_ultimo = "incorrecto"
                st.rerun()

        # Mostrar retroalimentación si ya envió la respuesta en esta pregunta
        if st.session_state.get("respondido", False):
            if st.session_state.resultado_ultimo == "correcto":
                st.success("¡Correcto! 🎉")
            else:
                st.error("❌ No es exacto.")
                st.write(f"**Lo que era:** {ej_actual['en']}")
                st.write(f"**Lo que pusiste:** {st.session_state.get('input_' + str(st.session_state.paso), '')}")

            st.write(f"**Traducción:** {ej_actual['es']}")

            if st.button("Siguiente pregunta ➡️"):
                st.session_state.paso += 1
                st.session_state.respondido = False
                st.rerun()

    else:
        # Pantalla final
        st.balloons()
        st.success("¡Prueba finalizada!")
        st.write(
            f"Tu calificación final: **{st.session_state.puntuacion} de {total_preguntas}** aciertos."
        )

        if st.button("🔄 Configurar nuevo test"):
            st.session_state.configurado = False
            st.rerun()
