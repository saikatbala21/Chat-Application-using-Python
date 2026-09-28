import socket
import threading
from tkinter import *


def send(listbox, entry):
    message = entry.get()
    if message:
        listbox.insert('end', "Client: " + message)
        entry.delete(0, END)
        # Send message to server
        try:
            s.send(bytes(message, "utf-8"))
        except Exception as e:
            listbox.insert('end', "Error: Could not send message.")


def receive_messages(listbox):
    """Background loop to catch messages from the server."""
    while True:
        try:
            server_message = s.recv(1024)
            if not server_message:
                break
            listbox.insert('end', "Server: " + server_message.decode("utf-8"))
        except:
            # Handle disconnection or errors
            listbox.insert('end', "Disconnected from server.")
            break


# UI Setup
window = Tk()
window.title("Client")

listbox = Listbox(window, width=50)
listbox.pack(padx=5, pady=5)

entry = Entry(window, width=50)
entry.pack(side="bottom", padx=5, pady=5)

# Bind 'Enter' key to send message for better UX
entry.bind("<Return>", lambda x: send(listbox, entry))

button = Button(window, text="Send", command=lambda: send(listbox, entry))
button.pack(side="bottom", padx=5, pady=5)

# Socket Setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_NAME = socket.gethostname()
port = 12345

try:
    s.connect((HOST_NAME, port))
    print("Connected to server.")

    # Start the receiving thread
    # daemon=True ensures the thread dies when the window is closed
    receive_thread = threading.Thread(target=receive_messages, args=(listbox,), daemon=True)
    receive_thread.start()
except Exception as e:
    listbox.insert('end', "Failed to connect to server.")

window.mainloop()
