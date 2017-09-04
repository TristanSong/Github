import bluetooth

devices = bluetooth.find_service(address="34:02:86:DA:8A:CB")

for device in devices:
    if device["protocol"] == "RFCOMM":
        print(device["port"])
