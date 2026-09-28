import socket
import threading
from tkinter import *


def send(listbox, entry, client):
    message = entry.get()
    if message:
        listbox.insert('end', "Server: " + message)
        entry.delete(0, END)
        client.send(bytes(message, "utf-8"))


def receive_messages(listbox, client):
    """Threaded function to constantly listen for messages."""
    while True:
        try:
            client_message = client.recv(1024)
            if not client_message:
                break
            listbox.insert('end', "Client: " + client_message.decode("utf-8"))
        except:
            break


def start_server(listbox, button, entry):
    """Threaded function to handle connection without freezing the GUI."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST_NAME = socket.gethostname()
    port = 12345
    s.bind((HOST_NAME, port))
    s.listen(5)

    listbox.insert('end', "Waiting for connection...")
    client, address = s.accept()
    listbox.insert('end', f"Connected to {address}")

    # Enable the send button once connected
    button.config(command=lambda: send(listbox, entry, client))

    # Start a background thread to receive messages continuously
    receive_thread = threading.Thread(target=receive_messages, args=(listbox, client), daemon=True)
    receive_thread.start()


# GUI Setup
window = Tk()
window.title("Server")

listbox = Listbox(window, width=50)
listbox.pack(padx=5, pady=5)

entry = Entry(window, width=50)
entry.pack(side="bottom", padx=5, pady=5)

send_button = Button(window, text="Send")
send_button.pack(side="bottom", padx=5, pady=5)

# Start the server setup in a background thread
# This prevents the window from being 'Not Responding' while waiting for a client
init_thread = threading.Thread(target=start_server, args=(listbox, send_button, entry), daemon=True)
init_thread.start()

window.mainloop()
