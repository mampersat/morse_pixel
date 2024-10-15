from umqtt.simple import MQTTClient

import ubinascii
import machine
import neopixel
import json
import utime

import wifi

# Global variables (don't judge me)
client = None
button_value = 0

# PICO pin parameters
neopixel_pin = 28
button_pin_gpio = 27


# MQTT Server Parameters
BROKER = "broker.hivemq.com"
CLIENT_ID = "com/mampersat/proto_board" # ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC = b"com/mampersat/morsepixel"

# The unique name of the pixel we are controlling
CONTROLLED_PIXEL = "eilly" # the number on the morse code key device
LOCAL_COLOR = (10, 20, 30) # the color of the pixel when the button is pressed locally, a light blue

# The list of pixels we want to display
PIXELS = [CONTROLLED_PIXEL, "J-38"] # map pixels to neopixel locations starting at position 1

# Initialize the pin and NeoPixel
button_pin = machine.Pin(button_pin_gpio, machine.Pin.IN, machine.Pin.PULL_UP)
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), 10) # TODO if you have more than 10 pixels, change this

# Callback when a message is received
def sub_cb(topic, msg):

    msg_json = json.loads(msg)
    pixel = msg_json['pixel']

    if pixel not in PIXELS:
        print(f"Invalid pixel: {pixel}")
        return
    
    location = PIXELS.index(pixel) + 1 # 1-based index, 0 index is control pixel
    state = msg_json['state']
    
    color = (255, 0, 0)
    if 'color' in msg_json:
        color = msg_json['color']
        print(f"Setting pixel {pixel} to {color}")

    if state == "pressed":
        np[location] = tuple(color)
        np.write()

    if state == "released":
        np[location] = (0, 0, 0)
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
        np[0] = LOCAL_COLOR
        np.write()
        message = {"pixel": CONTROLLED_PIXEL, "state": "pressed", "color": LOCAL_COLOR}
        client.publish(MQTT_TOPIC, json.dumps(message))
        print("Sent: pressed")

    else:
        np[0] = (0, 0, 0)
        np.write()
        message = {"pixel": CONTROLLED_PIXEL, "state": "released"}
        client.publish(MQTT_TOPIC, json.dumps(message))
        print("Sent: released")


def main():
    print("Starting main loop")
    global client

    button_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler = handle_button_pin_change)

    client = MQTTClient(CLIENT_ID, BROKER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(MQTT_TOPIC)

    last_connect_time = utime.time()

    while True:
        # Blocking wait for message, swallowing exceptions
        try:
            client.check_msg()
        except Exception as e:
            print(f"Error: {e}")

        # Reconnect to the broker every 10min
        if utime.time() - last_connect_time > 600:
            print("Reconnecting to broker")

            # attempt to connect with exponential back off
            for i in range(32): # 100 years... come find me in 100yrs and complain if this is a problem
                try:
                    client.connect()
                    client.subscribe(MQTT_TOPIC)
                    last_connect_time = utime.time()
                    break
                except:
                    print(f"Failed to connect. Retrying in {2**i} seconds")
                    utime.sleep(2**i)

main()