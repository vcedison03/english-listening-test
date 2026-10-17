from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

st.set_page_config(
    page_title="Test de Listening en Inglés", page_icon="🎧", layout="centered"
)

# --- ESTILO CSS CON FONDO DE LA BANDERA DE GRAN BRETAÑA ---
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
        background-color: rgba(255, 255, 255, 0.92);
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

# Banco de vocabulario
sujetos = [
    ("The teacher", "El profesor"),
    ("A student", "Un estudiante"),
    ("My friend", "Mi amigo"),
    ("The chef", "El chef"),
    ("An artist", "Un artista"),
    ("Our neighbor", "Nuestro vecino"),
    ("The doctor", "El doctor"),
    ("A mechanic", "Un mecánico"),
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


def generar_frase_aleatoria():
  tiempo_tipo = random.choice(
      ["Presente Simple", "Futuro Simple", "Presente Continuo"]
  )
  sujeto_en, sujeto_es = random.choice(sujetos)

  if tiempo_tipo == "Presente Simple":
    verbo_en, verbo_es = random.choice(verbos_presente)
    obj_en, obj_es = random.choice(objetos)
    lugar_en, lugar_es = random.choice(lugares)
    en = f"{sujeto_en} {verbo_en} {obj_en} {lugar_en}."
    es = f"{sujeto_es} {verbo_es} {obj_es} {lugar_es}."

  elif tiempo_tipo == "Futuro Simple":
    verbo_en, verbo_es = random.choice(verbos_futuro)
    obj_en, obj_es = random.choice(objetos)
    en = f"{sujeto_en} will {verbo_en} {obj_en} tomorrow."
    es = f"{sujeto_es} {verbo_es} {obj_es} mañana."

  else:  # Presente Continuo
    verbo_en, verbo_es = random.choice(
        [("working on", "trabajando en"), ("studying", "estudiando")]
    )
    obj_en, obj_es = random.choice(objetos)
    en = f"{sujeto_en} is {verbo_en} {obj_en} right now."
    es = f"{sujeto_es} está {verbo_es} {obj_es} ahora mismo."

  return {"tiempo": tiempo_tipo, "en": en, "es": es}


def obtener_audio_bytes(texto):
  tts = gTTS(text=texto, lang="en")
  fp = BytesIO()
  tts.write_to_fp(fp)
  fp.seek(0)
  return fp.read()


TOTAL_PREGUNTAS = 5

# Inicializar estado de la sesión
if "paso" not in st.session_state:
  st.session_state.paso = 0
  st.session_state.puntuacion = 0
  st.session_state.ej_actual = generar_frase_aleatoria()
  st.session_state.respondido = False
  st.session_state.historial = []

# Flujo de la prueba
if st.session_state.paso < TOTAL_PREGUNTAS:
  st.subheader(
      f"Pregunta {st.session_state.paso + 1} de {TOTAL_PREGUNTAS}"
  )
  st.info(f"Tiempo verbal: **{st.session_state.ej_actual['tiempo']}**")

  # Reproductor de audio
  audio_bytes = obtener_audio_bytes(st.session_state.ej_actual["en"])
  st.audio(audio_bytes, format="audio/mp3")

  # Formulario de entrada
  if not st.session_state.respondido:
    with st.form(key=f"form_{st.session_state.paso}"):
      respuesta = st.text_input("Escribe lo que escuchaste en inglés:")
      submit_button = st.form_submit_button(label="Enviar respuesta")

      if submit_button:
        limpia_original = (
            st.session_state.ej_actual["en"].rstrip("?.!").lower()
        )
        limpia_respuesta = respuesta.rstrip("?.!").lower()

        st.session_state.respondido = True
        st.session_state.ultima_respuesta = respuesta

        if limpia_respuesta == limpia_original:
          st.session_state.puntuacion += 1
          st.session_state.es_correcto = True
        else:
          st.session_state.es_correcto = False

        # Guardamos la pregunta y los bytes del audio para el repaso final
        st.session_state.historial.append({
            "pregunta": st.session_state.paso + 1,
            "tiempo": st.session_state.ej_actual["tiempo"],
            "original": st.session_state.ej_actual["en"],
            "usuario": respuesta,
            "traduccion": st.session_state.ej_actual["es"],
            "correcto": st.session_state.es_correcto,
            "audio": audio_bytes,
        })
        st.rerun()

  # Retroalimentación inmediata
  if st.session_state.respondido:
    if st.session_state.es_correcto:
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
  # Pantalla final
  st.balloons()
  st.success("¡Prueba finalizada!")

  promedio = (st.session_state.puntuacion / TOTAL_PREGUNTAS) * 100

  # Definición de Niveles de Calificación
  if promedio == 100:
    nivel = "🏆 Nivel Avanzado (Excelente)"
    mensaje_nivel = (
        "¡Increíble! Tienes una comprensión auditiva perfecta."
    )
  elif promedio >= 80:
    nivel = "🥇 Nivel Intermedio - Alto"
    mensaje_nivel = "¡Muy bien! Comprendes casi la totalidad del vocabulario."
  elif promedio >= 60:
    nivel = "🥈 Nivel Intermedio - Básico"
    mensaje_nivel = "Buen trabajo. Reconoces las frases pero debes afinar detalles de ortografía."
  elif promedio >= 40:
    nivel = "🥉 Nivel En Desarrollo"
    mensaje_nivel = (
        "Vas por buen camino. Necesitas practicar más la escucha diaria."
    )
  else:
    nivel = "📘 Nivel Principiante"
    mensaje_nivel = (
        "¡Sigue practicando! Repasa el vocabulario y vuelve a intentarlo."
    )

  # Mostrar resultados principales
  st.metric(
      label="Calificación Final",
      value=f"{st.session_state.puntuacion} / {TOTAL_PREGUNTAS}",
      delta=f"{promedio:.0f}% de aciertos",
  )
  st.subheader(nivel)
  st.info(mensaje_nivel)

  st.divider()
  st.subheader("📋 Repaso detallado con audio")

  # Mostrar historial con la opción de escuchar nuevamente el audio
  for item in st.session_state.historial:
    if item["correcto"]:
      st.markdown(f"✅ **Pregunta {item['pregunta']} ({item['tiempo']})**")
    else:
      st.markdown(f"❌ **Pregunta {item['pregunta']} ({item['tiempo']})**")

    st.write(f"- **Frase original:** `{item['original']}`")
    st.write(f"- **Tu respuesta:** `{item['usuario']}`")
    st.write(f"- **Traducción:** {item['traduccion']}")

    # Reproductor de audio para repaso
    st.audio(item["audio"], format="audio/mp3")
    st.markdown("---")

  # Botón para repetir el test
  if st.button("🔄 Repetir la prueba completa"):
    st.session_state.paso = 0
    st.session_state.puntuacion = 0
    st.session_state.ej_actual = generar_frase_aleatoria()
    st.session_state.respondido = False
    st.session_state.historial = []
    st.rerun()
