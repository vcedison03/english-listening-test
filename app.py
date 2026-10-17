from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Test de Listening en Inglés", page_icon="🎧", layout="centered"
)

# --- ESTILO CSS PARA EL FONDO DE LA BANDERA DE GRAN BRETAÑA ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), 
                          url("https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .block-container {
        background-color: rgba(255, 255, 255, 0.93);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    h1, h2, h3, p, label {
        color: #111111 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎧 Test de Listening Dinámico")
st.write(
    "Escucha el audio generado y escribe exactamente la frase en inglés que escuchas."
)

# Banco de vocabulario por categorías
sujetos = [
    ("The teacher", "El profesor"),
    ("A student", "Un estudiante"),
    ("My friend", "Mi amigo"),
    ("The chef", "El chef"),
    ("An artist", "Un artista"),
    ("Our neighbor", "Nuestro vecino"),
    ("The doctor", "El doctor"),
    ("A mechanic", "Un mecánico"),
    ("The engineer", "El ingeniero"),
    ("The pilot", "El piloto"),
]

objetos = [
    ("a book", "un libro"),
    ("a house", "una casa"),
    ("a car", "un carro"),
    ("a project", "un proyecto"),
    ("a report", "un informe"),
    ("a song", "una canción"),
    ("a letter", "una carta"),
]

lugares_complementos = [
    ("in the morning", "por la mañana"),
    ("at home", "en casa"),
    ("in the office", "en la oficina"),
    ("every day", "todos los días"),
    ("at the station", "en la estación"),
]


def generar_frase_aleatoria():
    tiempos = [
        "Presente Simple",
        "Presente Continuo",
        "Presente Perfecto",
        "Presente Perfecto Continuo",
        "Pasado Simple",
        "Pasado Continuo",
        "Pasado Perfecto",
        "Pasado Perfecto Continuo",
        "Futuro Simple (Will)",
        "Futuro Continuo",
        "Futuro Perfecto",
        "Futuro Perfecto Continuo",
    ]

    tiempo_tipo = random.choice(tiempos)
    sujeto_en, sujeto_es = random.choice(sujetos)
    obj_en, obj_es = random.choice(objetos)
    lugar_en, lugar_es = random.choice(lugares_complementos)

    if tiempo_tipo == "Presente Simple":
        v_en, v_es = random.choice([("reads", "lee"), ("paints", "pinta"), ("cleans", "limpia")])
        en = f"{sujeto_en} {v_en} {obj_en} {lugar_en}."
        es = f"{sujeto_es} {v_es} {obj_es} {lugar_es}."

    elif tiempo_tipo == "Presente Continuo":
        v_en, v_es = random.choice([("reading", "leyendo"), ("preparing", "preparando"), ("cleaning", "limpiando")])
        en = f"{sujeto_en} is {v_en} {obj_en} right now."
        es = f"{sujeto_es} está {v_es} {obj_es} ahora mismo."

    elif tiempo_tipo == "Presente Perfecto":
        v_en, v_es = random.choice([("finished", "terminado"), ("prepared", "preparado"), ("written", "escrito")])
        en = f"{sujeto_en} has {v_en} {obj_en} today."
        es = f"{sujeto_es} ha {v_es} {obj_es} hoy."

    elif tiempo_tipo == "Presente Perfecto Continuo":
        v_en, v_es = random.choice([("studying", "estudiando"), ("working on", "trabajando en")])
        en = f"{sujeto_en} has been {v_en} {obj_en} for two hours."
        es = f"{sujeto_es} ha estado {v_es} {obj_es} durante dos horas."

    elif tiempo_tipo == "Pasado Simple":
        v_en, v_es = random.choice([("bought", "compró"), ("built", "construyó"), ("found", "encontró")])
        en = f"{sujeto_en} {v_en} {obj_en} yesterday."
        es = f"{sujeto_es} {v_es} {obj_es} ayer."

    elif tiempo_tipo == "Pasado Continuo":
        v_en, v_es = random.choice([("reading", "leyendo"), ("preparing", "preparando")])
        en = f"{sujeto_en} was {v_en} {obj_en} when I arrived."
        es = f"{sujeto_es} estaba {v_es} {obj_es} cuando llegué."

    elif tiempo_tipo == "Pasado Perfecto":
        v_en, v_es = random.choice([("completed", "completado"), ("prepared", "preparado")])
        en = f"{sujeto_en} had {v_en} {obj_en} before the meeting."
        es = f"{sujeto_es} había {v_es} {obj_es} antes de la reunión."

    elif tiempo_tipo == "Pasado Perfecto Continuo":
        v_en, v_es = random.choice([("organizing", "organizando"), ("reviewing", "revisando")])
        en = f"{sujeto_en} had been {v_en} {obj_en} all morning."
        es = f"{sujeto_es} había estado {v_es} {obj_es} toda la mañana."

    elif tiempo_tipo == "Futuro Simple (Will)":
        v_en, v_es = random.choice([("buy", "comprará"), ("build", "construirá"), ("organize", "organizará")])
        en = f"{sujeto_en} will {v_en} {obj_en} tomorrow."
        es = f"{sujeto_es} {v_es} {obj_es} mañana."

    elif tiempo_tipo == "Futuro Continuo":
        v_en, v_es = random.choice([("using", "usando"), ("preparing", "preparando")])
        en = f"{sujeto_en} will be {v_en} {obj_en} at this time tomorrow."
        es = f"{sujeto_es} estará {v_es} {obj_es} a esta hora mañana."

    elif tiempo_tipo == "Futuro Perfecto":
        v_en, v_es = random.choice([("finished", "terminado"), ("delivered", "entregado")])
        en = f"{sujeto_en} will have {v_en} {obj_en} by next week."
        es = f"{sujeto_es} habrá {v_es} {obj_es} para la próxima semana."

    else:  # Futuro Perfecto Continuo
        v_en, v_es = random.choice([("working on", "trabajando en"), ("studying", "estudiando")])
        en = f"{sujeto_en} will have been {v_en} {obj_en} for five years."
        es = f"{sujeto_es} habrá estado {v_es} {obj_es} durante cinco años."

    return {"tiempo": tiempo_tipo, "en": en, "es": es}


def obtener_audio_bytes(texto):
    tts = gTTS(text=texto, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


# Inicializar el estado de la sesión para la prueba
TOTAL_PREGUNTAS = 5

if "paso" not in st.session_state:
    st.session_state.paso = 0
    st.session_state.puntuacion = 0
    st.session_state.ej_actual = generar_frase_aleatoria()
    st.session_state.respondido = False
    st.session_state.resultado_ultimo = None
    st.session_state.historial = []

# Si la prueba no ha terminado
if st.session_state.paso < TOTAL_PREGUNTAS:
    st.subheader(f"Pregunta {st.session_state.paso + 1} de {TOTAL_PREGUNTAS}")
    st.info(f"Tiempo verbal: **{st.session_state.ej_actual['tiempo']}**")

    # Generar audio con gTTS y reproducirlo en Streamlit
    audio_bytes = obtener_audio_bytes(st.session_state.ej_actual["en"])
    st.audio(audio_bytes, format="audio/mp3")

    # Formulario de respuesta
    if not st.session_state.respondido:
        with st.form(key=f"form_{st.session_state.paso}"):
            respuesta = st.text_input(
                "Escribe lo que escuchaste en inglés:", key=f"input_{st.session_state.paso}"
            )
            submit_button = st.form_submit_button(label="Enviar respuesta")

            if submit_button:
                limpia_original = st.session_state.ej_actual["en"].rstrip("?.!").lower()
                limpia_respuesta = respuesta.rstrip("?.!").lower()

                st.session_state.respondido = True
                st.session_state.ultima_respuesta = respuesta
                
                if limpia_respuesta == limpia_original:
                    st.session_state.puntuacion += 1
                    st.session_state.resultado_ultimo = "correcto"
                else:
                    st.session_state.resultado_ultimo = "incorrecto"

                # Guardar en historial con su audio para el repaso
                st.session_state.historial.append({
                    "pregunta": st.session_state.paso + 1,
                    "tiempo": st.session_state.ej_actual["tiempo"],
                    "original": st.session_state.ej_actual["en"],
                    "usuario": respuesta,
                    "traduccion": st.session_state.ej_actual["es"],
                    "correcto": st.session_state.resultado_ultimo == "correcto",
                    "audio": audio_bytes,
                })
                st.rerun()

    # Mostrar retroalimentación si ya envió la respuesta en esta pregunta
    if st.session_state.respondido:
        if st.session_state.resultado_ultimo == "correcto":
            st.success("¡Correcto! 🎉")
        else:
            st.error("❌ No es exacto.")
            st.write(f"**Lo que era:** {st.session_state.ej_actual['en']}")
            st.write(f"**Lo que pusiste:** {st.session_state.ultima_respuesta}")

        st.write(f"**Traducción:** {st.session_state.ej_actual['es']}")

        if st.button("Siguiente pregunta ➡️"):
            st.session_state.paso += 1
            st.session_state.respondido = False
            if st.session_state.paso < TOTAL_PREGUNTAS:
                st.session_state.ej_actual = generar_frase_aleatoria()
            st.rerun()

else:
    # Pantalla final, promedio y repaso con audio
    st.balloons()
    st.success("¡Prueba finalizada!")

    promedio = (st.session_state.puntuacion / TOTAL_PREGUNTAS) * 100

    if promedio == 100:
        nivel = "🏆 Nivel Avanzado (Excelente)"
        mensaje = "¡Comprensión auditiva perfecta!"
    elif promedio >= 80:
        nivel = "🥇 Nivel Intermedio - Alto"
        mensaje = "¡Gran trabajo! Comprendes casi todos los tiempos verbales."
    elif promedio >= 60:
        nivel = "🥈 Nivel Intermedio - Básico"
        mensaje = "Buen desempeño. Reconoces estructuras principales."
    else:
        nivel = "📘 Nivel Principiante / En Desarrollo"
        mensaje = "Sigue practicando para reconocer tiempos compuestos más complejos."

    st.metric(
        label="Calificación Final",
        value=f"{st.session_state.puntuacion} / {TOTAL_PREGUNTAS}",
        delta=f"{promedio:.0f}% de aciertos",
    )
    st.subheader(nivel)
    st.info(mensaje)

    st.divider()
    st.subheader("📋 Repaso detallado (puedes volver a escuchar el audio)")

    for item in st.session_state.historial:
        if item["correcto"]:
            st.markdown(f"✅ **Pregunta {item['pregunta']} - {item['tiempo']}**")
        else:
            st.markdown(f"❌ **Pregunta {item['pregunta']} - {item['tiempo']}**")

        st.write(f"- **Frase original:** `{item['original']}`")
        st.write(f"- **Tu respuesta:** `{item['usuario']}`")
        st.write(f"- **Traducción:** {item['traduccion']}")
        
        # Audio disponible para volver a escuchar
        st.audio(item["audio"], format="audio/mp3")
        st.markdown("---")

    if st.button("🔄 Reiniciar test"):
        st.session_state.paso = 0
        st.session_state.puntuacion = 0
        st.session_state.ej_actual = generar_frase_aleatoria()
        st.session_state.respondido = False
        st.session_state.resultado_ultimo = None
        st
