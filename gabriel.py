#import bluetooth
###
# Configura o objeto do adaptador Bluetooth
#bt_adapter = bluetooth.Bluetooth()

# Verifica se o adaptador está disponível
#if bt_adapter.available():

    # Inicia o scan de dispositivos BLE
#    bt_adapter.start_scan(10)

    # Aguarda até que os dispositivos sejam encontrados
#    while bt_adapter.ble_scan_active():
#        bt_devices = bt_adapter.get_discovered_devices()

        # Exibe informações sobre os dispositivos encontrados
#        for device in bt_devices:
#            print("Dispositivo encontrado: %s, endereço: %s" % (device.name, device.address))

    # Para o scan de dispositivos BLE
#    bt_adapter.stop_scan()
#else:
#    print("Adaptador Bluetooth indisponível.")
def main():
    print("Fala ai rapaziada")
if __name__ == "__main__":
    main()