import bluetooth, subprocess
import sys
import time

# target bluetooth name, address, RFCOMM port, password
target_name = "JBL GO"
target_address = None
target_port = []
target_passwd = "0000"


nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True, flush_cache=True, lookup_class=False)
for device in nearby_devices:
    if target_name == device[1]:
        target_address = device[0]
        print(device)
        break

if target_address is not None:
    print("target_address found!\nbuilding connection......")
    """
    services = bluetooth.find_service(address=target_address)
    if services != []:
        for service in services:
            if service["protocol"] == "RFCOMM":
                target_port.append(service["port"])
        #print(target_port)
    else:    
        print("Services not found!")
        time.sleep(3)
        sys.exit()
    """
    # kill any "bluetooth-agent" process that is already running
    subprocess.call("kill -9 'pidof bluetooth-agent'", shell=True)
    # start a new "bluetooth-agent" process where target_passwd is the password
    status = subprocess.call("bluetooth-agent" + target_passwd + "&", shell=True)
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((target_address, 1))
        print("connection built!")
    except bluetooth.btcommon.BluetoothError as err:
        print("connection error!")
else:
    print("target_address not found!")


