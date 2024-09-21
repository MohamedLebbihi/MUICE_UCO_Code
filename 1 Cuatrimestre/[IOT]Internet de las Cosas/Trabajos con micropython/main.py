##########################################################################
# Mohamed Lebbihi (z32lelem) Y Arbi Sardi Zakaria Nour el islem (z22zazaa)
##########################################################################
import network
import time
from machine import ADC, Pin, PWM
import math
from umqtt.simple import MQTTClient

# Configuration du Wi-Fi
SSID = 'Wokwi-GUEST'  # Réseau Wi-Fi ouvert sur Wokwi
PASSWORD = ''  # Pas de mot de passe pour Wokwi-GUEST

# Configuration du broker MQTT public HiveMQ
BROKER = 'broker.hivemq.com'  # URL du broker public HiveMQ
PORT = 1883  # Port pour une connexion non sécurisée
CLIENT_ID = 'esp32_client'
TOPIC_PUBLISH = b'joystick/couleur'
TOPIC_SUBSCRIBE = b'led/control'

# Fonction pour connecter l'ESP32 au Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Connexion en cours au réseau Wi-Fi...")
        time.sleep(1)
    
    print("Connecté au Wi-Fi", wlan.ifconfig())

# Fonction pour gérer les messages MQTT reçus
def mqtt_callback(topic, msg):
    print(f"Message reçu de {topic}: {msg}")
    if msg == b"rouge":
        set_led_color_by_mqtt("Rouge")
    elif msg == b"vert":
        set_led_color_by_mqtt("Vert")
    elif msg == b"bleu":
        set_led_color_by_mqtt("Bleu")

# Configurer la LED RGB avec PWM
led_red = PWM(Pin(14), freq=1000)
led_green = PWM(Pin(12), freq=1000)
led_blue = PWM(Pin(13), freq=1000)

# Fonction pour éteindre la LED RGB
def turn_off_led():
    led_red.duty(0)
    led_green.duty(0)
    led_blue.duty(0)
    print("LED éteinte")

# Fonction pour régler la couleur de la LED via MQTT
def set_led_color_by_mqtt(color):
    if color == "Rouge":
        led_red.duty(1023)
        led_green.duty(0)
        led_blue.duty(0)
        print("Couleur contrôlée via MQTT: Rouge")
    elif color == "Vert":
        led_red.duty(0)
        led_green.duty(1023)
        led_blue.duty(0)
        print("Couleur contrôlée via MQTT: Vert")
    elif color == "Bleu":
        led_red.duty(0)
        led_green.duty(0)
        led_blue.duty(1023)
        print("Couleur contrôlée via MQTT: Bleu")
    else:
        turn_off_led()

# Fonction pour calculer l'angle du joystick
def get_angle(x, y):
    x_centered = x - 2048
    y_centered = y - 2048
    angle = math.atan2(y_centered, x_centered)
    angle_degrees = math.degrees(angle)
    if angle_degrees < 0:
        angle_degrees += 360
    return angle_degrees

# Fonction pour déterminer la couleur à afficher en fonction de l'angle
def set_led_color(angle):
    if 0 <= angle < 120:
        led_red.duty(1023)
        led_green.duty(0)
        led_blue.duty(0)
        publish_mqtt("Rouge")
    elif 120 <= angle < 240:
        led_red.duty(0)
        led_green.duty(1023)
        led_blue.duty(0)
        publish_mqtt("Vert")
    else:
        led_red.duty(0)
        led_green.duty(0)
        led_blue.duty(1023)
        publish_mqtt("Bleu")

# Fonction pour publier la couleur actuelle via MQTT
def publish_mqtt(color):
    msg = f"Couleur actuelle: {color}"
    client.publish(TOPIC_PUBLISH, msg.encode())
    print(f"Message publié: {msg}")

# Configuration du joystick
horz = ADC(Pin(34))
vert = ADC(Pin(35))
sel = Pin(27, Pin.IN, Pin.PULL_UP)
CENTER_THRESHOLD = 100

# Fonction principale pour lire le joystick et contrôler la LED
def read_joystick():
    x_pos = horz.read()
    y_pos = vert.read()
    if abs(x_pos - 2048) < CENTER_THRESHOLD and abs(y_pos - 2048) < CENTER_THRESHOLD:
        turn_off_led()
    else:
        angle = get_angle(x_pos, y_pos)
        set_led_color(angle)

# Connexion au Wi-Fi
connect_wifi()

# Configuration du client MQTT
client = MQTTClient(CLIENT_ID, BROKER, port=PORT)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(TOPIC_SUBSCRIBE)
print(f"Connecté au broker MQTT {BROKER}, souscrit au topic {TOPIC_SUBSCRIBE}")

# Boucle principale
while True:
    read_joystick()
    client.check_msg()  # Vérifier si des messages MQTT sont reçus
    time.sleep(0.2)
