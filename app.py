from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

st.set_page_config(
    page_title="Test Completo de Listening", page_icon="🎧", layout="centered"
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

st.title("🎧 Test de Listening Avanzado")
st.write(
    "Escucha el audio generado y escribe exactamente la frase en inglés que escuchas."
)

# ==========================================
# BANCO EXTENSO DE VOCABULARIO Y ESTRUCTURAS
# ==========================================

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
    ("My sister", "Mi hermana"),
    ("The scientist", "El científico"),
    ("A writer", "Un escritor"),
    ("The manager", "El gerente"),
]

objetos = [
    ("a book", "un libro"),
    ("a house", "una casa"),
    ("a car", "un carro"),
    ("a new project", "un nuevo proyecto"),
    ("a report", "un informe"),
    ("a song", "una canción"),
    ("a meal", "una comida"),
    ("a letter", "una carta"),
    ("a website", "un sitio web"),
    ("a plan", "un plan"),
]

lugares_tiempos = [
    ("in the office", "en la oficina"),
    ("at home", "en casa"),
    ("in the morning", "por la mañana"),
    ("every day", "todos los días"),
    ("at the station", "en la estación"),
    ("in the city", "en la ciudad"),
    ("during the meeting", "durante la reunión"),
]


def generar_frase_aleatoria():
  # Los 12 tiempos verbales de la gramática inglesa
  tiempos = [
      "Present Simple",
      "Present Continuous",
      "Present Perfect",
      "Present Perfect Continuous",
      "Past Simple",
      "Past Continuous",
      "Past Perfect",
      "Past Perfect Continuous",
      "Future Simple (Will)",
      "Future Continuous",
      "Future Perfect",
      "Future Perfect Continuous",
  ]

  tiempo_tipo = random.choice(tiempos)
  sujeto_en, sujeto_es = random.choice(sujetos)
  obj_en, obj_es = random.choice(objetos)
  lugar_en, lugar_es = random.choice(lugares_tiempos)

  # Generación de la estructura gramatical según el tiempo
  if tiempo_tipo == "Present Simple":
    verbos = [
        ("reads", "lee"),
        ("prepares", "prepara"),
        ("paints", "pinta"),
        ("cleans", "limpia"),
        ("writes", "escribe"),
        ("inspects", "inspecciona"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} {v_en} {obj_en} {lugar_en}."
    es = f"{sujeto_es} {v_es} {obj_es} {lugar_es}."

  elif tiempo_tipo == "Present Continuous":
    verbos = [
        ("reading", "leyendo"),
        ("preparing", "preparando"),
        ("painting", "pintando"),
        ("cleaning", "limpiando"),
        ("designing", "diseñando"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} is {v_en} {obj_en} right now."
    es = f"{sujeto_es} está {v_es} {obj_es} ahora mismo."

  elif tiempo_tipo == "Present Perfect":
    verbos = [
        ("finished", "terminado"),
        ("prepared", "preparado"),
        ("bought", "comprado"),
        ("built", "construido"),
        ("written", "escrito"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} has {v_en} {obj_en} today."
    es = f"{sujeto_es} ha {v_es} {obj_es} hoy."

  elif tiempo_tipo == "Present Perfect Continuous":
    verbos = [
        ("studying", "estudiando"),
        ("working on", "trabajando en"),
        ("building", "construyendo"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} has been {v_en} {obj_en} for two hours."
    es = f"{sujeto_es} ha estado {v_es} {obj_es} durante dos horas."

  elif tiempo_tipo == "Past Simple":
    verbos = [
        ("bought", "compró"),
        ("built", "construyó"),
        ("painted", "pintó"),
        ("cleaned", "limpió"),
        ("found", "encontró"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} {v_en} {obj_en} yesterday."
    es = f"{sujeto_es} {v_es} {obj_es} ayer."

  elif tiempo_tipo == "Past Continuous":
    verbos = [
        ("reading", "leyendo"),
        ("preparing", "preparando"),
        ("cleaning", "limpiando"),
        ("fixing", "reparando"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} was {v_en} {obj_en} when I arrived."
    es = f"{sujeto_es} estaba {v_es} {obj_es} cuando llegué."

  elif tiempo_tipo == "Past Perfect":
    verbos = [
        ("completed", "completado"),
        ("prepared", "preparado"),
        ("sold", "vendido"),
        ("written", "escrito"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} had {v_en} {obj_en} before the meeting."
    es = f"{sujeto_es} había {v_es} {obj_es} antes de la reunión."

  elif tiempo_tipo == "Past Perfect Continuous":
    verbos = [
        ("developing", "desarrollando"),
        ("organizing", "organizando"),
        ("reviewing", "revisando"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} had been {v_en} {obj_en} all morning."
    es = f"{sujeto_es} había estado {v_es} {obj_es} toda la mañana."

  elif tiempo_tipo == "Future Simple (Will)":
    verbos = [
        ("buy", "comprará"),
        ("build", "construirá"),
        ("organize", "organizará"),
        ("present", "presentará"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} will {v_en} {obj_en} tomorrow."
    es = f"{sujeto_es} {v_es} {obj_es} mañana."

  elif tiempo_tipo == "Future Continuous":
    verbos = [
        ("using", "usando"),
        ("preparing", "preparando"),
        ("reviewing", "revisando"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} will be {v_en} {obj_en} at this time tomorrow."
    es = f"{sujeto_es} estará {v_es} {obj_es} a esta hora mañana."

  elif tiempo_tipo == "Future Perfect":
    verbos = [
        ("finished", "terminado"),
        ("delivered", "entregado"),
        ("completed", "completado"),
    ]
    v_en, v_es = random.choice(verbos)
    en = f"{sujeto_en} will have {v
