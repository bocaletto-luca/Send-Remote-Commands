# Software Name: Send Remote Commands
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# License: GPLv3

import tkinter as tk
import tkinter.messagebox as messagebox
import socket

# Creazione della finestra principale
window = tk.Tk()
window.title("Invia Comandi Remoti")

# Etichetta per il titolo
title_label = tk.Label(window, text="Invia Comandi Remoti", font=("Helvetica", 16))
title_label.pack()

# Etichette e campi di input per l'indirizzo IP del server, la porta, il nome utente e la password
ip_label = tk.Label(window, text="Indirizzo IP del Server:")
ip_label.pack()
ip_entry = tk.Entry(window)
ip_entry.pack()

port_label = tk.Label(window, text="Porta del Server:")
port_label.pack()
port_entry = tk.Entry(window)
port_entry.pack()

username_label = tk.Label(window, text="Nome Utente:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")  # Usa 'show' per nascondere la password
password_entry.pack()

# Pulsante per connettersi al server (nella finestra principale)
connect_button = tk.Button(window, text="Connetti al Server")
connect_button.pack()

# Etichetta per lo stato della connessione (nella finestra principale)
status_label = tk.Label(window, text="")
status_label.pack()

# Etichetta e campo di input per inviare comandi (nella finestra principale)
command_label = tk.Label(window, text="Comando:")
command_label.pack()
command_entry = tk.Entry(window)
command_entry.pack()

# Pulsante per inviare comandi (nella finestra principale)
send_button = tk.Button(window, text="Invia Comando")
send_button.pack()

# Etichetta per la risposta del server (nella finestra principale)
response_label = tk.Label(window, text="Risposta del Server:")
response_label.pack()
response_text = tk.Text(window, height=10, width=40)
response_text.pack()
response_text.config(state=tk.DISABLED)

# Inizializzazione del socket client
client_socket = None

# Funzione per connettersi al server remoto con autenticazione
def connect_to_server():
    global client_socket
    server_ip = ip_entry.get()
    server_port_str = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    try:
        server_port = int(server_port_str)
    except ValueError:
        messagebox.showerror("Errore", "La porta deve essere un numero intero.")
        return

    if not server_ip or not server_port_str or not username or not password:
        messagebox.showerror("Errore", "Inserisci un indirizzo IP valido, una porta, un nome utente e una password.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        # Invia nome utente e password al server per l'autenticazione
        dati_autenticazione = f"{username}:{password}"
        client_socket.send(dati_autenticazione.encode())
        risposta = client_socket.recv(1024).decode()

        if risposta == "Autenticato":
            status_label.config(text="Connesso al server")
            connect_button.config(state=tk.DISABLED)
        else:
            status_label.config(text="Autenticazione fallita")
            client_socket.close()
    except Exception as e:
        status_label.config(text=f"Errore di connessione: {str(e)}")

# Pulsante per connettersi al server (nella finestra principale)
connect_button.config(command=connect_to_server)

# Funzione per inviare comandi al server remoto
def send_command():
    comando = command_entry.get()
    if comando:
        try:
            client_socket.send(comando.encode())
            risposta = client_socket.recv(1024).decode()
            response_text.config(state=tk.NORMAL)
            response_text.delete(1.0, tk.END)  # Cancella il testo esistente
            response_text.insert(tk.END, risposta)
            response_text.config(state=tk.DISABLED)
        except Exception as e:
            response_text.config(state=tk.NORMAL)
            response_text.delete(1.0, tk.END)
            response_text.insert(tk.END, f"Errore: {str(e)}")
            response_text.config(state=tk.DISABLED)

# Pulsante per inviare comandi (nella finestra principale)
send_button.config(command=send_command)

# Ciclo GUI principale
window.mainloop()
