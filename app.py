from io import BytesIO
import random
import difflib
from gtts import gTTS
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Test de Listening Dinámico", page_icon="🎧", layout="centered"
)

st.title("🎧 Test de Listening Dinámico con Gramática")
st.write(
    "Practica tu comprensión auditiva con oraciones generadas dinámicamente."
)

# ==========================================
# CONFIGURACIÓN EN LA BARRA LATERAL
# ==========================================
st.sidebar.header("⚙️ Configuración")

# Nivel de exigencia (estilo del segundo código)
nivel = st.sidebar.selectbox(
    "Nivel de exigencia:", ["Estricto (90%)", "Medio (75%)", "Flexible (60%)"]
)
if "Estricto" in nivel:
  umbral_exito = 90.0
elif "Flexible" in nivel:
  umbral_exito = 60.0
else:
  umbral_exito = 75.0

# Modo de cantidad de preguntas
st.sidebar.markdown("---")
modo_cantidad = st.sidebar.radio(
    "Modo de cantidad de preguntas:", ["Número específico", "Indefinido"]
)
if modo_cantidad == "Número específico":
  cantidad_preguntas = st.sidebar.number_input(
      "¿Cuántas preguntas deseas responder?",
      min_value=1,
      max_value=100,
      value=5,
      step=1,
  )
else:
  cantidad_preguntas = "Indefinido"

# ==========================================
# BANCO DE VOCABULARIO
# ==========================================
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


# ==========================================
# INICIALIZACIÓN DEL ESTADO DE LA SESIÓN
# ==========================================
if "iniciado" not in st.session_state:
  st.session_state.iniciado = False
if "idx" not in st.session_state:
  st.session_state.idx = 0
if "historial" not in st.session_state:
  st.session_state.historial = []
if "aciertos" not in st.session_state:
  st.session_state.aciertos = 0
if "suma_porcentajes" not in st.session_state:
  st.session_state.suma_porcentajes = 0.0
if "ej_actual" not in st.session_state:
  st.session_state.ej_actual = None
if "respondido" not in st.session_state:
  st.session_state.respondido = False
if "ultimo_resultado" not in st.session_state:
  st.session_state.ultimo_resultado = None
if "mostrar_resultados" not in st.session_state:
  st.session_state.mostrar_resultados = False

# Botón inicial para comenzar
if not st.session_state.iniciado:
  if st.button("🚀 Comenzar Test", type="primary"):
    st.session_state.iniciado = True
    st.session_state.idx = 0
    st.session_state.historial = []
    st.session_state.aciertos = 0
    st.session_state.suma_porcentajes = 0.0
    st.session_state.ej_actual = generar_frase_aleatoria()
    st.session_state.respondido = False
    st.session_state.mostrar_resultados = False
    st.rerun()

else:
  # Botón para terminar en cualquier momento en la barra lateral
  if not st.session_state.mostrar_resultados:
    st.sidebar.markdown("---")
    if st.sidebar.button("🛑 Terminar test y ver historial"):
      st.session_state.mostrar_resultados = True
      st.rerun()

  # Verificar si se acabaron las preguntas o se presionó terminar
  limite_alcanzado = (
      False
      if cantidad_preguntas == "Indefinido"
      else st.session_state.idx >= int(cantidad_preguntas)
  )

  if st.session_state.mostrar_resultados or limite_alcanzado:
    st.balloons()
    st.success("🎉 ¡Prueba finalizada con éxito!")
    st.markdown("---")
    st.subheader("=" * 10 + " RESULTADOS FINALES Y REVISIÓN " + "=" * 10)
    st.write(f"⚙️ **Nivel:** {nivel} (Umbral: {umbral_exito}%)")

    total_respuestas = len(st.session_state.historial)
    promedio = (
        st.session_state.suma_porcentajes / total_respuestas
        if total_respuestas > 0
        else 0
    )

    st.metric("📝 Preguntas respondidas", total_respuestas)
    st.metric(
        "✅ Aprobadas", f"{st.session_state.aciertos} de {total_respuestas}"
    )
    st.metric("📊 Precisión promedio", f"{promedio:.1f}%")

    st.markdown("---")
    st.subheader("📋 LISTADO DE ORACIONES PRACTICADAS:")

    if not st.session_state.historial:
      st.info("No hay oraciones registradas en el historial todavía.")
    else:
      for item in st.session_state.historial:
        with st.expander(
            f"Pregunta #{item['n']} ({item['calificacion']:.1f}% - {item['estado_str']})"
        ):
          st.write(f"**Original (EN):** {item['oracion']}")
          st.write(f"**Tu respuesta:** {item['respuesta']}")
          st.write(f"**Calificación:** {item['calificacion']:.1f}%")

    st.markdown("---")
    if st.button("🔄 Volver a empezar"):
      st.session_state.iniciado = False
      st.session_state.respondido = False
      st.session_state.mostrar_resultados = False
      st.rerun()

  else:
    # Pregunta en curso
    ej = st.session_state.ej_actual
    st.info(f"Tiempo verbal: **{ej['tiempo']}**")

    if cantidad_preguntas == "Indefinido":
      st.markdown(
          f"**Pregunta #{st.session_state.idx + 1} (Modo Indefinido)**"
      )
    else:
      st.markdown(
          f"**Pregunta #{st.session_state.idx + 1} de {int(cantidad_preguntas)}**"
      )

    # Generar y reproducir audio en memoria
    tts = gTTS(text=ej["en"], lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp.read(), format="audio/mp3")

    st.info(
        "🎧 Escucha el audio anterior y escribe exactamente la frase en inglés"
        " que escuchas."
    )

    if not st.session_state.respondido:
      with st.form(key=f"form_{st.session_state.idx}"):
        respuesta = st.text_input(
            "Tu respuesta en inglés:", key=f"input_{st.session_state.idx}"
        )
        enviar = st.form_submit_button("Calificar respuesta", type="primary")

        if enviar:
          if not respuesta.strip():
            st.warning("Por favor escribe una respuesta antes de calificar.")
          else:
            limpia_original = ej["en"].rstrip("?.!").lower()
            limpia_respuesta = respuesta.rstrip("?.!").lower()

            # Cálculo de similitud mediante difflib (compatible con el nivel de exigencia)
            similitud = (
                difflib.SequenceMatcher(
                    None, limpia_original, limpia_respuesta
                ).ratio()
                * 100
            )
            aprobado = similitud >= umbral_exito
            estado_str = (
                "¡Aprobado! ✅" if aprobado else "Por debajo del nivel ❌"
            )

            if aprobado:
              st.session_state.aciertos += 1

            st.session_state.suma_porcentajes += similitud

            st.session_state.historial.append({
                "n": st.session_state.idx + 1,
                "oracion": ej["en"],
                "respuesta": respuesta,
                "calificacion": similitud,
                "estado_str": estado_str,
            })

            st.session_state.ultimo_resultado = {
                "similitud": similitud,
                "estado_str": estado_str,
                "esperada": ej["en"],
                "traduccion": ej["es"],
                "respuesta": respuesta,
            }
            st.session_state.respondido = True
            st.rerun()
    else:
      res_u = st.session_state.ultimo_resultado
      st.success(
          f"Calificación: {res_u['similitud']:.1f}% -> {res_u['estado_str']}"
      )
      st.write(f"✍️ **Tu respuesta:** {res_u['respuesta']}")
      st.write(f"🎯 **Frase esperada:** {res_u['esperada']}")
      st.write(f"📖 **Traducción:** {res_u['traduccion']}")

      st.markdown("---")
      if st.button("Siguiente pregunta ➡️", type="primary"):
        st.session_state.idx += 1
        st.session_state.respondido = False
        st.session_state.ej_actual = generar_frase_aleatoria()
        st.rerun()
