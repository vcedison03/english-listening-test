import os
import random
import re
import time
import difflib
import requests
from deep_translator import GoogleTranslator
from gtts import gTTS
import streamlit as st

st.set_page_config(
    page_title="Práctica de Inglés con Libros", page_icon="📚", layout="centered"
)

# Inicializar estado de sesión
if "iniciado" not in st.session_state:
  st.session_state.iniciado = False
if "oraciones" not in st.session_state:
  st.session_state.oraciones = []
if "idx" not in st.session_state:
  st.session_state.idx = 0
if "total" not in st.session_state:
  st.session_state.total = 0
if "suma_porcentajes" not in st.session_state:
  st.session_state.suma_porcentajes = 0.0
if "aciertos" not in st.session_state:
  st.session_state.aciertos = 0
if "historial" not in st.session_state:
  st.session_state.historial = []
if "libro_titulo" not in st.session_state:
  st.session_state.libro_titulo = ""
if "tipo_exigencia" not in st.session_state:
  st.session_state.tipo_exigencia = ""
if "umbral_exito" not in st.session_state:
  st.session_state.umbral_exito = 75.0
if "audio_path" not in st.session_state:
  st.session_state.audio_path = None
if "oracion_actual" not in st.session_state:
  st.session_state.oracion_actual = ""
if "esperada" not in st.session_state:
  st.session_state.esperada = ""
if "significado_es" not in st.session_state:
  st.session_state.significado_es = ""
if "resultado_ultimo" not in st.session_state:
  st.session_state.resultado_ultimo = None


def cargar_oraciones(tema, min_pal, max_pal):
  try:
    res = requests.get(
        f"https://gutendex.com/books/?search={tema}&languages=en", timeout=25
    ).json()
  except Exception:
    return [], "Error de conexión"

  libros = res.get("results", [])
  if not libros:
    return [], "No se encontraron libros"

  libro = random.choice(libros)
  titulo = libro.get("title", "Desconocido")

  text_url = libro.get("formats", {}).get(
      "text/plain; charset=us-ascii"
  ) or libro.get("formats", {}).get("text/plain; charset=utf-8")
  if not text_url:
    return [], "El libro no tiene texto plano disponible"

  try:
    raw_text = requests.get(text_url, timeout=20).text
  except Exception:
    return [], "Error al descargar el texto del libro"

  text_clean = re.sub(r"\s+", " ", raw_text)
  oraciones = [
      o.strip()
      for o in re.split(r"(?<=[.!?])\s+", text_clean)
      if min_pal <= len(o.split()) <= max_pal
  ]
  random.shuffle(oraciones)
  return oraciones, titulo


# --- PANTALLA DE CONFIGURACIÓN ---
if not st.session_state.iniciado:
  st.title("📚 Práctica de Inglés: Test Interactivo")
  st.write(
      "Practica tu comprensión auditiva escuchando fragmentos de libros clásicos"
      " y escribiendo lo que comprendes."
  )

  nivel_op = st.selectbox(
      "Selecciona el nivel de exigencia:",
      ["Medio (75%)", "Estricto (90%)", "Flexible (60%)"],
  )
  if "Estricto" in nivel_op:
    umbral = 90.0
    tipo_exig = "Estricto"
  elif "Flexible" in nivel_op:
    umbral = 60.0
    tipo_exig = "Flexible"
  else:
    umbral = 75.0
    tipo_exig = "Medio"

  categoria = st.selectbox(
      "Selecciona categoría de libros:",
      [
          "Physics & Electromagnetism",
          "Astronomy & Space",
          "Technology & Computing",
          "Philosophy & Logic",
          "Tema personalizado",
      ],
  )

  temas_dict = {
      "Physics & Electromagnetism": "physics",
      "Astronomy & Space": "astronomy",
      "Technology & Computing": "technology",
      "Philosophy & Logic": "philosophy",
  }

  if categoria == "Tema personalizado":
    tema_custom = st.text_input(
        "Escribe tu tema en inglés:", value="science"
    )
    tema = tema_custom
  else:
    tema = temas_dict[categoria]

  col1, col2 = st.columns(2)
  with col1:
    min_p = st.number_input("Cantidad mínima de palabras:", value=6, min_value=3)
  with col2:
    max_p = st.number_input(
        "Cantidad máxima de palabras:", value=12, max_value=30
    )

  if st.button("🚀 Iniciar Test", type="primary"):
    with st.spinner("Buscando libro y extrayendo oraciones..."):
      oraciones, titulo = cargar_oraciones(tema, min_p, max_p)
      if not oraciones:
        st.error(
            f"No se encontraron oraciones con esa longitud ({titulo}). Intenta"
            " con otros parámetros."
        )
      else:
        st.session_state.oraciones = oraciones
        st.session_state.libro_titulo = titulo
        st.session_state.umbral_exito = umbral
        st.session_state.tipo_exigencia = tipo_exig
        st.session_state.iniciado = True
        st.session_state.idx = 0
        st.session_state.total = 0
        st.session_state.suma_porcentajes = 0.0
        st.session_state.aciertos = 0
        st.session_state.historial = []

        # Preparar primera oración
        oracion_act = st.session_state.oraciones[0]
        st.session_state.oracion_actual = oracion_act
        audio_name = "temp_audio.mp3"
        tts = gTTS(text=oracion_act, lang="en")
        tts.save(audio_name)
        st.session_state.audio_path = audio_name
        st.rerun()

else:
  # --- PANTALLA DE PREGUNTAS ---
  if st.session_state.idx < len(st.session_state.oraciones):
    st.subheader(
        f"Pregunta #{st.session_state.idx + 1} de"
        f" {len(st.session_state.oraciones)}"
    )
    st.markdown(f"📚 **Libro actual:** _{st.session_state.libro_titulo}_")

    st.write("🎧 **Escucha el audio y escribe lo que entendiste:**")
    if os.path.exists(st.session_state.audio_path):
      st.audio(st.session_state.audio_path, format="audio/mp3")

    idioma = st.selectbox(
        "¿Cómo responderás?",
        ["Español (es)", "Inglés (en (transcripción literal))"],
    )
    es_espanol = "Español" in idioma

    respuesta_usuario = st.text_input(
        "Escribe tu respuesta aquí:", key=f"input_{st.session_state.idx}"
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      if st.button("Calificar respuesta", type="success"):
        if not respuesta_usuario.strip():
          st.warning("⚠️ Por favor escribe una respuesta antes de calificar.")
        else:
          traductor = GoogleTranslator(source="en", target="es")
          esperada = ""
          significado_es = ""

          for intento in range(3):
            try:
              time.sleep(0.5 * (intento + 1))
              if es_espanol:
                esperada = traductor.translate(
                    st.session_state.oracion_actual
                )
              else:
                significado_es = traductor.translate(
                    st.session_state.oracion_actual
                )
              break
            except Exception:
              continue

          if not esperada:
            esperada = st.session_state.oracion_actual
          if not significado_es:
            significado_es = st.session_state.oracion_actual

          if es_espanol:
            similitud = (
                difflib.SequenceMatcher(
                    None, esperada.lower(), respuesta_usuario.lower()
                ).ratio()
                * 100
            )
          else:
            similitud = (
                difflib.SequenceMatcher(
                    None,
                    st.session_state.oracion_actual.lower(),
                    respuesta_usuario.lower(),
                ).ratio()
                * 100
            )

          if similitud >= st.session_state.umbral_exito:
            estado_str = "¡Aprobado! ✅"
            st.session_state.aciertos += 1
          else:
            estado_str = "Por debajo del nivel ❌"

          st.session_state.total += 1
          st.session_state.suma_porcentajes += similitud

          st.session_state.historial.append({
              "n": st.session_state.idx + 1,
              "oracion": st.session_state.oracion_actual,
              "respuesta": respuesta_usuario,
              "calificacion": similitud,
              "estado_str": estado_str,
              "audio_file": st.session_state.audio_path,
          })

          st.session_state.resultado_ultimo = {
              "resp": respuesta_usuario,
              "esp": esperada,
              "orig": st.session_state.oracion_actual,
              "sig": significado_es,
              "sim": similitud,
              "est": estado_str,
              "es_esp": es_espanol,
          }
          st.rerun()

    with col_btn2:
      if st.button("Terminar test y ver historial", type="secondary"):
        st.session_state.idx = len(st.session_state.oraciones)
        st.rerun()

    # Mostrar resultado si se acaba de calificar
    if st.session_state.resultado_ultimo:
      res_data = st.session_state.resultado_ultimo
      st.markdown("---")
      st.info("### Resumen de este punto")
      st.write(f"✍️ **Lo que escribiste:** {res_data['resp']}")
      if res_data["es_esp"]:
        st.write(f"🎯 **Lo que se esperaba (ES):** {res_data['esp']}")
        st.write(f"📖 **Oración original (EN):** {res_data['orig']}")
      else:
        st.write(f"🎯 **Lo que se esperaba (EN):** {res_data['orig']}")
        st.write(f"📖 **Significado en ES:** {res_data['sig']}")
      st.write(
          f"🎯 **Calificación:** {res_data['sim']:.1f}% ->"
          f" {res_data['est']}"
      )

      promedio_actual = (
          st.session_state.suma_porcentajes / st.session_state.total
          if st.session_state.total > 0
          else 0
      )
      st.write(
          f"📊 **Promedio total:** {promedio_actual:.1f}%"
          f" ({st.session_state.aciertos}/{st.session_state.total} aprobadas)"
      )

      if st.button("Siguiente oración ➡️", type="primary"):
        st.session_state.idx += 1
        st.session_state.resultado_ultimo = None
        if st.session_state.idx < len(st.session_state.oraciones):
          oracion_act = st.session_state.oraciones[st.session_state.idx]
          st.session_state.oracion_actual = oracion_act
          audio_name = f"audio_{st.session_state.idx}.mp3"
          tts = gTTS(text=oracion_act, lang="en")
          tts.save(audio_name)
          st.session_state.audio_path = audio_name
        st.rerun()

  else:
    # --- PANTALLA DE RESULTADOS FINALES ---
    st.title("🏁 Resultados Finales y Revisión")
    st.write(f"📚 **Libro:** {st.session_state.libro_titulo}")
    st.write(f"⚙️ **Nivel:** {st.session_state.tipo_exigencia}")
    st.write(f"📝 **Preguntas respondidas:** {st.session_state.total}")
    st.write(f"✅ **Aprobadas:** {st.session_state.aciertos}")

    if st.session_state.total > 0:
      prom_final = (
          st.session_state.suma_porcentajes / st.session_state.total
      )
      st.metric(
          label="Precisión Promedio Final", value=f"{prom_final:.1f}%"
      )

    st.markdown("---")
    st.subheader("📋 Listado de Oraciones Practicadas")
    for item in st.session_state.historial:
      st.markdown(
          f"**[#{item['n']}] Original (EN):** `{item['oracion']}`<br>Tu"
          f" respuesta: _{item['respuesta']}_ — **{item['calificacion']:.1f}%**"
          f" ({item['estado_str']})",
          unsafe_allow_html=True,
      )

    st.markdown("---")
    st.subheader("🎧 Modo Reproducción de Revisión")
    if st.session_state.historial:
      opciones_sel = {
          f"Oración #{item['n']}: {item['oracion'][:40]}...": item
          for item in st.session_state.historial
      }
      seleccion = st.selectbox(
          "Selecciona una oración para volver a escucharla:",
          list(opciones_sel.keys()),
      )
      if seleccion:
        item_elegido = opciones_sel[seleccion]
        st.write(f"**Texto completo:** {item_elegido['oracion']}")
        if os.path.exists(item_elegido["audio_file"]):
          st.audio(item_elegido["audio_file"], format="audio/mp3")

    if st.button("🔄 Reiniciar Test con Nuevas Preguntas"):
      st.session_state.iniciado = False
      st.session_state.resultado_ultimo = None
      st.rerun()
