import bluetooth
import aioble

# Adresse MAC de l'ESP32 cible
target_mac = 'xx:xx:xx:xx:xx:xx'

# Fonction pour rechercher les adresses MAC des périphériques environnants
async def get_surrounding_macs():
    surrounding_macs = []
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            surrounding_macs.append(result.address())
    return surrounding_macs

# Se connecter à l'ESP32 cible via Bluetooth
print("Connexion à l'ESP32 cible...")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_mac, 1))
print("Connecté à l'ESP32 cible")

# Récupérer les adresses MAC des périphériques environnants
surrounding_macs = asyncio.run(get_surrounding_macs())
print("Adresses MAC des périphériques environnants : ", surrounding_macs)

# Fermer la connexion Bluetooth
sock.close()
