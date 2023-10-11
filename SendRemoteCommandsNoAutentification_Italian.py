# Software Name: Send Remote Commands
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# License: GPLv3

import tkinter as tk
import tkinter.messagebox as messagebox
import socket

# Creazione della finestra principale
window = tk.Tk()
window.title("Send Remote Commands")

# Etichetta per il titolo
title_label = tk.Label(window, text="Send Remote Commands", font=("Helvetica", 16))
title_label.pack()

# Etichette e campi di input per l'indirizzo IP e la porta del server (nella finestra principale)
ip_label = tk.Label(window, text="IP del Server:")
ip_label.pack()
ip_entry = tk.Entry(window)
ip_entry.pack()

port_label = tk.Label(window, text="Porta del Server:")
port_label.pack()
port_entry = tk.Entry(window)
port_entry.pack()

# Bottone per la connessione al server (nella finestra principale)
connect_button = tk.Button(window, text="Connetti al Server")
connect_button.pack()

# Etichetta per lo stato della connessione (nella finestra principale)
status_label = tk.Label(window, text="")
status_label.pack()

# Etichetta e campo di input per l'invio dei comandi (nella finestra principale)
command_label = tk.Label(window, text="Comando:")
command_label.pack()
command_entry = tk.Entry(window)
command_entry.pack()

# Bottone per l'invio dei comandi (nella finestra principale)
send_button = tk.Button(window, text="Invia Comando")
send_button.pack()

# Etichetta per la risposta del server (nella finestra principale)
response_label = tk.Label(window, text="Risposta del Server:")
response_label.pack()
response_text = tk.Text(window, height=10, width=40)
response_text.pack()
response_text.config(state=tk.DISABLED)

# Inizializzazione della socket del client
client_socket = None

# Funzione per connettersi al server remoto
def connect_to_server():
    global client_socket
    server_ip = ip_entry.get()
    server_port_str = port_entry.get()
    
    try:
        server_port = int(server_port_str)
    except ValueError:
        messagebox.showerror("Errore", "La porta deve essere un numero intero.")
        return

    if not server_ip or not server_port_str:
        messagebox.showerror("Errore", "Inserisci un indirizzo IP e una porta validi.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        status_label.config(text="Connesso al server")
        connect_button.config(state=tk.DISABLED)
    except Exception as e:
        status_label.config(text=f"Errore di connessione: {str(e)}")

# Bottone per la connessione al server (nella finestra principale)
connect_button.config(command=connect_to_server)

# Funzione per inviare comandi al server remoto
def send_command():
    command = command_entry.get()
    if command:
        try:
            client_socket.send(command.encode())
            response = client_socket.recv(1024).decode()
            response_text.config(state=tk.NORMAL)
            response_text.delete(1.0, tk.END)  # Cancella il testo esistente
            response_text.insert(tk.END, response)
            response_text.config(state=tk.DISABLED)
        except Exception as e:
            response_text.config(state=tk.NORMAL)
            response_text.delete(1.0, tk.END)
            response_text.insert(tk.END, f"Errore: {str(e)}")
            response_text.config(state=tk.DISABLED)

# Bottone per l'invio dei comandi (nella finestra principale)
send_button.config(command=send_command)

# Loop principale della GUI
window.mainloop()
