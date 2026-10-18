from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Test de Listening en Inglés", page_icon="🎧", layout="centered"
)

st.title("🎧 Test de Listening Dinámico")
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


def generar_frase_aleatoria():
  tiempo_tipo = random.choice(
      ["Presente Simple", "Futuro Simple", "Presente Continuo"]
  )
  sujeto = random.choice(sujetos)

  if tiempo_tipo == "Presente Simple":
    verbo_en, verbo_es = random.choice(verbos_presente)
    obj_en, obj_es = random.choice(objetos)
    lugar_en, lugar_es = random.choice(lugares)
    en = f"{sujeto} {verbo_en} {obj_en} {lugar_en}."
    es = f"{sujeto} {verbo_es} {obj_es} {lugar_es}."

  elif tiempo_tipo == "Futuro Simple":
    verbo_en, verbo_es = random.choice(verbos_futuro)
    obj_en, obj_es = random.choice(objetos)
    en = f"{sujeto} will {verbo_en} {obj_en} tomorrow."
    es = f"{sujeto} {verbo_es} {obj_es} mañana."

  else:  # Presente Continuo
    verbo_en, verbo_es = random.choice(
        [("working on", "trabajando en"), ("studying", "estudiando")]
    )
    obj_en, obj_es = random.choice(objetos)
    en = f"{sujeto} is {verbo_en} {obj_en} right now."
    es = f"{sujeto} está {verbo_es} {obj_es} ahora mismo."

  return {"tiempo": tiempo_tipo, "en": en, "es": es}


# Inicializar el estado de la sesión para la prueba
TOTAL_PREGUNTAS = 5

if "paso" not in st.session_state:
  st.session_state.paso = 0
  st.session_state.puntuacion = 0
  st.session_state.ej_actual = generar_frase_aleatoria()
  st.session_state.respondido = False
  st.session_state.resultado_ultimo = None

# Si la prueba no ha terminado
if st.session_state.paso < TOTAL_PREGUNTAS:
  st.subheader(
      f"Pregunta {st.session_state.paso + 1} de {TOTAL_PREGUNTAS}"
  )
  st.info(f"Tiempo verbal: **{st.session_state.ej_actual['tiempo']}**")

  # Generar audio con gTTS y reproducirlo en Streamlit
  tts = gTTS(text=st.session_state.ej_actual["en"], lang="en")
  fp = BytesIO()
  tts.write_to_fp(fp)
  fp.seek(0)
  st.audio(fp.read(), format="audio/mp3")

  # Formulario de respuesta
  with st.form(key=f"form_{st.session_state.paso}"):
    respuesta = st.text_input(
        "Escribe lo que escuchaste en inglés:", key=f"input_{st.session_state.paso}"
    )
    submit_button = st.form_submit_button(label="Enviar respuesta")

    if submit_button:
      limpia_original = (
          st.session_state.ej_actual["en"].rstrip("?.!").lower()
      )
      limpia_respuesta = respuesta.rstrip("?.!").lower()

      st.session_state.respondido = True
      if limpia_respuesta == limpia_original:
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
      st.write(f"**Lo que era:** {st.session_state.ej_actual['en']}")
      st.write(f"**Lo que pusiste:** {st.session_state.get('input_' + str(st.session_state.paso), '')}")

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
  st.write(
      f"Tu calificación final: **{st.session_state.puntuacion} de {TOTAL_PREGUNTAS}** aciertos."
  )

  if st.button("🔄 Reiniciar test"):
    st.session_state.paso = 0
    st.session_state.puntuacion = 0
    st.session_state.ej_actual = generar_frase_aleatoria()
    st.session_state.respondido = False
    st.rerun()
