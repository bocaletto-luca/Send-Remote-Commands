# Software Name: Send Remote Commands
# Author: Bocaletto Luca
# Website: https://www.elektronoide.it
# License: GPLv3

import tkinter as tk
import tkinter.messagebox as messagebox
import socket

# Creating the main window
window = tk.Tk()
window.title("Send Remote Commands")

# Label for the title
title_label = tk.Label(window, text="Send Remote Commands", font=("Helvetica", 16))
title_label.pack()

# Labels and input fields for the server's IP address and port (in the main window)
ip_label = tk.Label(window, text="Server IP:")
ip_label.pack()
ip_entry = tk.Entry(window)
ip_entry.pack()

port_label = tk.Label(window, text="Server Port:")
port_label.pack()
port_entry = tk.Entry(window)
port_entry.pack()

# Button to connect to the server (in the main window)
connect_button = tk.Button(window, text="Connect to Server")
connect_button.pack()

# Label for the connection status (in the main window)
status_label = tk.Label(window, text="")
status_label.pack()

# Label and input field for sending commands (in the main window)
command_label = tk.Label(window, text="Command:")
command_label.pack()
command_entry = tk.Entry(window)
command_entry.pack()

# Button to send commands (in the main window)
send_button = tk.Button(window, text="Send Command")
send_button.pack()

# Label for the server's response (in the main window)
response_label = tk.Label(window, text="Server Response:")
response_label.pack()
response_text = tk.Text(window, height=10, width=40)
response_text.pack()
response_text.config(state=tk.DISABLED)

# Initializing the client socket
client_socket = None

# Function to connect to the remote server
def connect_to_server():
    global client_socket
    server_ip = ip_entry.get()
    server_port_str = port_entry.get()
    
    try:
        server_port = int(server_port_str)
    except ValueError:
        messagebox.showerror("Error", "Port must be an integer.")
        return

    if not server_ip or not server_port_str:
        messagebox.showerror("Error", "Please enter a valid IP address and port.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        status_label.config(text="Connected to the server")
        connect_button.config(state=tk.DISABLED)
    except Exception as e:
        status_label.config(text=f"Connection error: {str(e)}")

# Button to connect to the server (in the main window)
connect_button.config(command=connect_to_server)

# Function to send commands to the remote server
def send_command():
    command = command_entry.get()
    if command:
        try:
            client_socket.send(command.encode())
            response = client_socket.recv(1024).decode()
            response_text.config(state=tk.NORMAL)
            response_text.delete(1.0, tk.END)  # Clear existing text
            response_text.insert(tk.END, response)
            response_text.config(state=tk.DISABLED)
        except Exception as e:
            response_text.config(state=tk.NORMAL)
            response_text.delete(1.0, tk.END)
            response_text.insert(tk.END, f"Error: {str(e)}")
            response_text.config(state=tk.DISABLED)

# Button to send commands (in the main window)
send_button.config(command=send_command)

# Main GUI loop
window.mainloop()
