from umqtt.simple import MQTTClient

import ubinascii
import machine
import neopixel
import time
import utime


# Global variables (don't judge me)
client = None
button_value = 0

# PICO pin parameters
neopixel_pin = 28
button_pin_gpio = 27

# MQTT Server Parameters
BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC = b"com/mampersat/morsepixel"

# Initialize the pin and NeoPixel
button_pin = machine.Pin(button_pin_gpio, machine.Pin.IN, machine.Pin.PULL_UP)
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), 2) # TODO when more clients change this

# Callback when a message is received
def sub_cb(topic, msg):
    print(f"Received: {msg}")

    if msg == b"pressed":
        np[1] = (255, 0, 0)
        np.write()

    if msg == b"released":
        np[1] = (0, 0, 0)
        np.write()

# Callback when the button is pressed
def handle_button_pin_change(pin):
    global mode, button_value

    # Did the value change?
    value = pin.value()
    if value == button_value:
        return

    button_value = value

    if value == 0:
        np[0] = (255, 0, 0)
        np.write()
        client.publish(MQTT_TOPIC, b"pressed")
        print("Snet: pressed")

    else:
        np[0] = (0, 0, 0)
        np.write()
        client.publish(b"com/mampersat/morsepixel", b"released")
        print("Sent: released")


def main():
    print("Starting main loop")
    global client

    button_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler = handle_button_pin_change)

    client = MQTTClient(CLIENT_ID, BROKER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    while True:
        # Blocking wait for message
        client.wait_msg()

main()            