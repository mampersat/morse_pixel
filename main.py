from umqtt.simple import MQTTClient
import ubinascii

import machine
import neopixel
import wifi
import time
import random
import utime

# PICO pin parameters
lights = 10
neopixel_pin = 28
brake_pin_gpio = 16
button_pin_gpio = 27

# MQTT Server Parameters
BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC = b"com/mampersat/morsepixel"
TCP_PORT = 1883
WEBSOCKET_PORT = 8000
TLS_TCP_PORT = 8883
TLS_WEBSOCKET_PORT = 8884

# Button/Brake states
button_value = 0
tap_counter = 0
tap_start_time = utime.ticks_ms()

# Initialize the pin and NeoPixel
button_pin = machine.Pin(button_pin_gpio, machine.Pin.IN, machine.Pin.PULL_UP)
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), lights)

# Callback when a message is received
def sub_cb(topic, msg):
    print("Inside callback")
    print((topic, msg))
    return True
    # if the message is pressed, turn on the LED
    if msg == b"pressed":
        print("LED ON")
        led.fill((255, 255, 255))
        led.write()


# Setup MQTT Client and Subscribe
def mqtt_subscribe():
    client = MQTTClient(CLIENT_ID, BROKER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Connected to %s, subscribed to %s topic" % (BROKER, MQTT_TOPIC))
    
    return client


def handle_button_pin_change(pin):
    global mode, button_value

    # Did the value change?
    value = pin.value()
    if value == button_value:
        return

    button_value = value

    if value == 0:
        print("Button pressed")
        np[0] = (255, 0, 0)
        np.write()
        client.publish(b"com/mampersat/morsepixel", b"pressed")

    else:
        print("Button released")
        np[0] = (0, 0, 0)
        np.write()
        client.publish(b"com/mampersat/morsepixel", b"released")

button_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler = handle_button_pin_change)

# Run the MQTT subscription
# TODO: Make the light blink first
client = mqtt_subscribe()

while True:
    # think about the future
    print("Hello, World!")
    time.sleep(1)
