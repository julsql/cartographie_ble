from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Dispositivo encontrado:", dev.addr)
        elif isNewData:
            print("Dados novos do dispositivo:", dev.addr)

        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print("Dispositivo %s (%s), endereço %s, RSSI=%d dB" % (dev.addr, dev.addrType, dev.getValueText(9), dev.rssi))

    for (adtype, desc, value) in dev.getScanData():
        print("  %s = %s" % (desc, value))

    if dev.servicesResolved:
        for svc in dev.services:
            print("Serviço encontrado: %s, UUID = %s" % (svc.uuid.getCommonName(), svc.uuid))

            for ch in svc.getCharacteristics():
                print("  Característica encontrada: %s, UUID = %s" % (ch.uuid.getCommonName(), ch.uuid))
