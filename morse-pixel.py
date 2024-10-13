import curses
from pynput import keyboard
import threading
import paho.mqtt.client as mqtt
import uuid

# Initialize the spacebar state
spacebar_pressed = False
remote_pressed = False

# MQTT Server Parameters
BROKER = "broker.hivemq.com"
CLIENT_ID = uuid.getnode() # unique ID for this client
MQTT_TOPIC = "com/mampersat/morsepixel"
mqtt_status = 'unconnected'

def on_connect(client, userdata, flags, reason_code, properties):
    global mqtt_status
    # print(f"Connected with result code {reason_code}")
    mqtt_status = f"Connected with result code {reason_code}"
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    global remote_pressed
    # print(msg.topic+" "+str(msg.payload))

    if msg.payload == b"pressed":
        remote_pressed = True

    if msg.payload == b"released":
        remote_pressed = False

def on_press(key):
    global spacebar_pressed, client
    if key == keyboard.Key.space:
        spacebar_pressed = True
        client.publish(MQTT_TOPIC, b"pressed")


def on_release(key):
    global spacebar_pressed
    if key == keyboard.Key.space:
        spacebar_pressed = False
        client.publish(MQTT_TOPIC, b"released")

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





