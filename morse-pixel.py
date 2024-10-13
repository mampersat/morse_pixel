import curses
from pynput import keyboard
import threading

# Initialize the spacebar state
spacebar_pressed = False
remote_pressed = False

def on_press(key):
    global spacebar_pressed
    if key == keyboard.Key.space:
        spacebar_pressed = True

def on_release(key):
    global spacebar_pressed
    if key == keyboard.Key.space:
        spacebar_pressed = False

def start_key_listener():
    # Start the pynput listener in a separate thread
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main(stdscr):
    global spacebar_pressed, remote_pressed

    # Clear the screen and set up the UI
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking input mode
    stdscr.addstr(0, 0, "Press SPACEBAR to see status.")
    stdscr.addstr(1, 0, "Press 'q' to quit.")

    while True:
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
