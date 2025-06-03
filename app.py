from flask import Flask, render_template, request
import random
import time
import pyttsx3
import threading
import serial
import serial.tools.list_ports

app = Flask(__name__)

# Diccionario de respuestas
respuestas = {
    "clima": "El cambio climático es la alteración a largo plazo del clima de la Tierra, especialmente en temperaturas, lluvias, vientos y fenómenos extremos.",
    "einstein": "Albert Einstein fue un físico teórico alemán, considerado uno de los científicos más importantes y conocidos de la historia.",
    "arduino": "Arduino es una plataforma de electrónica abierta que permite crear proyectos interactivos de forma fácil, combinando hardware (placas electrónicas) y software (un programa para escribir y cargar código).",
    "cielo": "El color del cielo suele ser azul durante el día, debido a un fenómeno llamado dispersión de Rayleigh: las moléculas del aire dispersan la luz solar, y el azul es el color que más se dispersa en la atmósfera.",
    "china": "La Gran Muralla China mide aproximadamente 21,196 kilómetros de largo, según estudios realizados por la Administración Estatal del Patrimonio Cultural de China en 2012.",
    "hormigas": "No, una persona no puede sobrevivir solo comiendo hormigas y sin agua. A corto plazo puede resistir unos días, pero sufrirá deshidratación severa y desnutrición.",
    "sanidad": "Las largas esperas se deben a la alta demanda de pacientes y servicios, falta de personal sanitario, recortes presupuestarios, gestión ineficiente y desigualdad geográfica.",
    "tusi": "El tusi es una droga sintética y peligrosa, que mezcla varias sustancias psicoactivas. Su consumo es muy riesgoso porque no se controla qué contiene ni cómo afecta.",
    "sudar": "Sí, puedes sudar bajo el agua, pero no lo notas ni te enfría como en el aire, porque el sudor se mezcla con el agua enseguida.",
    "caballos": "Los caballos duermen de pie para descansar ligeramente, pero necesitan acostarse un rato cada día para un sueño profundo y reparador.",
    "trabajo": "Monje. Tenías comida, techo, acceso a libros y educación. Además no ibas a la guerra ni trabajabas en el campo. Muchos monjes eran los intelectuales de su época.",
    "amor": "El amor es una fuerza emocional profunda que nos conecta con otros, da sentido a nuestras relaciones y muchas veces, a la vida misma.",
    "chiste": "¿Cuál es el colmo de un preso?........................................¡Tener libertad de expresión!",
    "youtube": "NO VAS A CREER QUIÉN TE INVITA A UN CAFÉ, ¡QUÉDATE HASTA EL FINAL!” “¡Hola, qué tal, bienvenidos al canal! Hoy te traigo algo diferente...YouTube quiere invitarte a un café , pero antes… ¡dale like, suscríbete y activa la campanita!",
    "opinion": "Tu opinión es como una pestaña en el ojo: molesta, inesperada y completamente innecesaria.",
    "insultame": "Vuestra presencia es como la peste: nadie la desea, todos la notan, y pocos sobreviven ilesos.",
}

#
contador = 0
ultimo_tiempo = time.time()
nivel = 0.0
TIEMPO_LIMITE = 20  # segundos sin preguntas para iniciar descenso

# 🔍 Función para detectar Arduino automáticamente
def detectar_arduino():
    print("Buscando puertos serie...")
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        print(f"- {puerto.device}: {puerto.description}")
        if "Arduino" in puerto.description or "CH340" in puerto.description or "USB" in puerto.description:
            try:
                arduino = serial.Serial(puerto.device, 9600, timeout=1)
                time.sleep(2)
                print(f"✅ Arduino detectado en {puerto.device}")
                return arduino
            except Exception as e:
                print(f"⚠️ No se pudo abrir {puerto.device}: {e}")
    print("❌ No se detectó ningún Arduino.")
    return None

arduino = detectar_arduino()

# 🔊 Enviar nivel de intensidad al buzzer (PWM)
def enviar_a_arduino(nivel_actual):
    if arduino and arduino.is_open:
        intensidad = int(nivel_actual * 255)
        intensidad = max(0, min(intensidad, 255))
        try:
            arduino.write(bytes([intensidad]))
            print(f"🎵 Buzzer -> nivel {nivel_actual:.2f}, intensidad {intensidad}")
        except Exception as e:
            print("⚠️ Error al enviar al Arduino:", e)

# 🧠 Deteriorar texto según el nivel
def deteriorar(texto, nivel):
    return ' '.join([
        palabra[::-1] + random.choice(["@", "#", "*", "~"]) if random.random() < nivel else palabra
        for palabra in texto.split()
    ])

# ⏬ Hilo que baja el nivel si no se pregunta
def decrementar_nivel():
    global nivel
    while True:
        time.sleep(1)
        ahora = time.time()
        if ahora - ultimo_tiempo > TIEMPO_LIMITE:
            if nivel > 0:
                nivel = max(0, nivel - 0.05)
                enviar_a_arduino(nivel)

threading.Thread(target=decrementar_nivel, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    global contador, ultimo_tiempo, nivel

    respuesta_final = ""
    ahora = time.time()

    if request.method == "POST":
        pregunta = request.form["pregunta"].lower().strip()
        base = "No tengo una respuesta para eso."

        for clave in respuestas:
            if clave in pregunta:
                base = respuestas[clave]
                break

        contador += 1
        ultimo_tiempo = ahora
        nivel = min(contador * 0.1, 1.0)  # Sube máximo a 100%
        enviar_a_arduino(nivel)

        respuesta_final = deteriorar(base, nivel)

        def hablar(texto):
            motor = pyttsx3.init()
            motor.setProperty('rate', 150)
            motor.say(texto)
            motor.runAndWait()

        threading.Thread(target=hablar, args=(respuesta_final,)).start()

    return render_template("index.html", respuesta=respuesta_final, nivel=int(nivel * 100))

if __name__ == "__main__":
    app.run(debug=True)

    
try:
    # Abrir el puerto COM3 a 9600 baudios (ajusta si usas otro puerto o velocidad)
    ser = serial.Serial('COM3', 9600, timeout=1)
    print("Puerto abierto")

    # Aquí haces la comunicación con el Arduino
    ser.write(b'Hola Arduino\n')  # ejemplo de envío
    time.sleep(1)
    respuesta = ser.readline()
    print("Respuesta:", respuesta)

finally:
    # Esto siempre se ejecuta: cierra el puerto para liberar el recurso
    if ser.is_open:
        ser.close()
        print("Puerto cerrado")