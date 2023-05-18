#Une liste des MAC address d'exemple, avec des modifications pour visualizer s'il va répetir les valeurs ou pas
# Supprimer pour utiliser l'officiel
tree = {'7C:DF:A1:E8:6B:CA': ['45:E5:DF:77:D8:DF', 'C9:6C:98:68:E8:F8', '0F:8E:6E:11:CD:A4', '66:BA:B9:88:55:3D', 'C9:6C:98:68:E8:F6', '58:33:43:87:37:A7', '5A:1D:01:57:8B:34', '00:A7:0A:B6:91:B8', 'F9:7B:EA:EB:39:F8', 'C5:CB:94:48:95:23', '00:6F:F2:C0:AE:4D'], 'C9:6C:98:68:E8:F6': [], '58:33:43:87:37:A7': [], '75:58:CE:9F:BA:27': [], '3D:F7:F5:44:98:7D': [], '7C:DF:A1:E7:D0:66': ['1F:8E:6E:11:CD:A4', '4A:1D:01:57:8B:34', 'C9:6C:97:68:E8:F6', '45:E5:DF:77:D8:DF', '66:BA:B9:88:55:3D', '7C:DF:A1:E8:6B:CA', '58:33:43:87:37:A7', '00:6F:F2:C0:AE:4D', 'C9:6C:98:68:E8:F8', '00:A7:0A:B6:91:B8', 'F9:7B:EA:EB:39:F8', 'C5:CB:94:48:95:23'], 'F9:7B:EA:EB:39:F8': [], '00:A7:0A:B6:91:B8': [], 'C1:97:B1:C7:50:8E': [], '10:94:97:09:00:EC': [], 'C9:6C:98:68:E8:F8': [], '6E:C3:13:14:44:10': [], '51:50:72:55:D5:4C': [], '68:14:DE:F5:83:0D': [], 'E4:1D:FE:50:EF:1A': [], '65:91:C1:97:1A:0E': [], '45:E5:DF:77:D8:DF': [], '66:BA:B9:88:55:3D': [], '00:6F:F2:C0:AE:4D': [], '5A:1D:01:57:8B:34': [], 'D0:D2:45:69:46:C1': [], '55:05:ED:E4:6C:7A': [], '0F:8E:6E:11:CD:A4': [], 'C5:CB:94:48:95:23': []}


def print_tree(tree, level=0, printed_devices=None):
    if printed_devices is None:
        printed_devices = set()                                     #Crée l'ensemble

    if isinstance(tree, dict):                                      #Montre la liste complète des dispositifs trouvés                 
        print('Liste des dispositifs trouvés \n')
        for mac, devices in tree.items():                       
            indent = '  ' * level
            if mac not in printed_devices:
                print(f'{indent}{mac}')
                printed_devices.add(mac)

            if devices:                                             #S'il scan l'autre ESP, montre la liste des dispositifs trouvés par cela
                print("Les dispositifs trouvés par cet ESP")
                print_tree(devices, level+1, printed_devices)
    elif isinstance(tree, list):
        for device in tree:
            indent = '  ' * level
            if device not in printed_devices:                       #Vérifie si le dispositif a déjà été imprimé et l'ajoute à l'ensemble
                print(f'{indent}{device}')
                printed_devices.add(device)




print_tree(tree)

