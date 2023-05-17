import random

def gerar_esp32_aleatoria(num_esp, num_aparelhos):
    esp32_scan = []
    for i in range(num_esp):
        esp_id = f'ESP32_{i+1}'
        num_conectados = random.randint(0, num_aparelhos)
        aparelhos = [f'MAC{j+1}' for j in range(num_conectados)]
        esp_dict = {esp_id: aparelhos}
        esp32_scan.append(esp_dict)
    return esp32_scan

num_esp = 3
num_aparelhos = 5

esp32_scan = gerar_esp32_aleatoria(num_esp, num_aparelhos)
print(esp32_scan)

def exibir_scan_esp32(scan):
    for esp in scan:
        for esp_id, aparelhos in esp.items():
            print(esp_id + ':')
            for aparelho in aparelhos:
                print('  ' + aparelho)

print('Scan ESP32:')
exibir_scan_esp32(esp32_scan)