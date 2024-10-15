import curses
from pynput import keyboard
import threading
import paho.mqtt.client as mqtt
import uuid
import json

# Initialize the spacebar state
spacebar_pressed = False
remote_pressed = []

# MQTT Server Parameters
BROKER = "broker.hivemq.com"
CLIENT_ID = uuid.getnode() # unique ID for this client
MQTT_TOPIC = "com/mampersat/morsepixel"

# The unique name of the pixel we are controlling
CONTROLLED_PIXEL = "eilly" # the number on the morse code key device
LOCAL_COLOR = (30, 20, 10) # the color of the pixel when the button is pressed locally, a light blue

# The list of pixels we want to display
pixels = {
    CONTROLLED_PIXEL: 0,
    "J-38": 0
}

mqtt_status = 'unconnected'

def on_connect(client, userdata, flags, reason_code, properties):
    global mqtt_status
    # print(f"Connected with result code {reason_code}")
    mqtt_status = f"Connected with result code {reason_code}"
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    global remote_pressed, mqtt_status
    mqtt_status = msg.payload
    return

    msg_json = json.loads(msg.payload)
    pixel = msg_json['pixel']

    if pixel not in pixels:
        print(f"Invalid pixel: {pixel}")
        return
    
    location = pixels.index(pixel) + 1 # 1-based index, 0 index is control pixel
    state = msg_json['state']

    if state == b"pressed":
        remote_pressed = True

    if state == b"released":
        remote_pressed = False

def on_press(key):
    global spacebar_pressed, client
    if key == keyboard.Key.space:
        spacebar_pressed = True
        message = {"pixel": CONTROLLED_PIXEL, "state": "pressed", "color": LOCAL_COLOR}
        client.publish(MQTT_TOPIC, json.dumps(message))

def on_release(key):
    global spacebar_pressed
    if key == keyboard.Key.space:
        spacebar_pressed = False
        message = {"pixel": CONTROLLED_PIXEL, "state": "released"}
        client.publish(MQTT_TOPIC, json.dumps(message))

def start_key_listener():
    # Start the pynput listener in a separate thread
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main(stdscr):
    global spacebar_pressed, remote_pressed, mqtt_status, client

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()

    # Clear the screen and set up the UI
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking input mode
    stdscr.addstr(0, 0, "Press SPACEBAR to see status.")
    stdscr.addstr(1, 0, "Press 'q' to quit.")

    while True:
        # Display MQTT connection status
        # status_text = "MQTT:   ●" if mqtt_status == "Connected" else "MQTT:   ◯"
        status_text = f"MQTT: {mqtt_status}"
        stdscr.addstr(2, 0, status_text)

        # Display the current button status
        status_text = "Local:  ●" if spacebar_pressed else "Local:  ◯"
        stdscr.addstr(3, 0, status_text)

        status_text = "Remote: ●" if remote_pressed else "Remote: ◯"
        stdscr.addstr(4, 0, status_text)

        # Refresh the screen to update content
        stdscr.refresh()

        # Check for user input to quit the UI
        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":
    # Start the keyboard listener in a separate thread
    listener_thread = threading.Thread(target=start_key_listener, daemon=True)
    listener_thread.start()

    # Start the curses UI
    curses.wrapper(main)





