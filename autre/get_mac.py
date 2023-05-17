import machine
import ubinascii

# Récupérer l'adresse MAC de l'ESP32
mac = ubinascii.hexlify(machine.unique_id(), ':').decode()

# Afficher l'adresse MAC
print('Adresse MAC de l\'ESP32:', mac)
