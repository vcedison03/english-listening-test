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

    elif tiempo_tipo == "Futuro Simple (Will
