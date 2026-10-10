import sys
!{sys.executable} -m pip install gtts

from io import BytesIO
import random
from gtts import gTTS
from IPython.display import Audio, display

from io import BytesIO
import random
from gtts import gTTS
from IPython.display import Audio, display

# Banco de vocabulario por categorías
sujetos = ["The teacher", "A student", "My friend", "The chef", "An artist", "Our neighbor", "The doctor", "A mechanic"]
verbos_presente = [("drinks", "toma"), ("prepares", "prepara"), ("reads", "lee"), ("paints", "pinta"), ("cleans", "limpia")]
verbos_futuro = [("visit", "visitará"), ("build", "construirá"), ("buy", "comprará"), ("learn", "aprenderá"), ("organize", "organizará")]
objetos = [("coffee", "café"), ("a book", "un libro"), ("a house", "una casa"), ("a car", "un carro"), ("a project", "un proyecto")]
lugares = [("in the morning", "por la mañana"), ("at home", "en casa"), ("in the office", "en la oficina"), ("every day", "todos los días")]

def generar_frase_aleatoria():
    tiempo_tipo = random.choice(["Presente Simple", "Futuro Simple", "Presente Continuo"])
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
        verbo_en, verbo_es = random.choice([("working on", "trabajando en"), ("studying", "estudiando")])
        obj_en, obj_es = random.choice(objetos)
        en = f"{sujeto} is {verbo_en} {obj_en} right now."
        es = f"{sujeto} está {verbo_es} {obj_es} ahora mismo."

    return {"tiempo": tiempo_tipo, "en": en, "es": es}

def reproducir_audio(texto):
    tts = gTTS(text=texto, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    display(Audio(fp.read(), autoplay=True))

# Parámetros del test
TOTAL_PREGUNTAS = 5
puntuacion = 0

print("==================================================")
print(f"  TEST DE LISTENING EN JUPYTER - {TOTAL_PREGUNTAS} PREGUNTAS DINÁMICAS")
print("==================================================")

for i in range(1, TOTAL_PREGUNTAS + 1):
    ej = generar_frase_aleatoria()
    
    print(f"\n--------------------------------------------------")
    print(f"Pregunta {i} de {TOTAL_PREGUNTAS} | Tiempo: [ {ej['tiempo']} ]")

    reproducir_audio(ej["en"])

    respuesta = input("Escucha el audio arriba. Escribe lo que escuchaste en inglés (o 'salir'): ").strip()

    if respuesta.lower() == "salir":
        print(f"\nPráctica interrumpida. Llevabas {puntuacion} aciertos.")
        break

    limpia_original = ej["en"].rstrip("?.!").lower()
    limpia_respuesta = respuesta.rstrip("?.!").lower()

    if limpia_respuesta == limpia_original:
        print("¡Correcto! 🎉")
        puntuacion += 1
    else:
        print("❌ No es exacto.")
        print(f"   Lo que era:    {ej['en']}")
        print(f"   Lo que pusiste: {respuesta}")

    print(f"   Traducción:    {ej['es']}")

print("\n==================================================")
print(f" Tu calificación final: {puntuacion} de {TOTAL_PREGUNTAS} aciertos.")
print("==================================================")

