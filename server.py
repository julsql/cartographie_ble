import socket

# Définir l'adresse IP de l'ESP32 et le numéro de port à écouter
ip_address = '0.0.0.0'  # écoute sur toutes les interfaces
port = 1234

# Créer une socket d'écoute TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip_address, port))
sock.listen(1)  # une seule connexion simultanée autorisée

print('En attente de connexion sur', ip_address, ':', port)

# Attendre qu'une connexion soit établie
conn, addr = sock.accept()
print('Connexion établie avec', addr)

# Recevoir des données de la connexion
data = conn.recv(1024)

# Afficher les données reçues
print('Données reçues:', data.decode())

# Fermer la connexion
conn.close()
