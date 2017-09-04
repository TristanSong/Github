import bluetooth, subprocess

addr = "38:1C:4A:A3:45:40"
port = 4
passkey = "1234"

subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)
status = subprocess.call("bluetooth-agent" + passkey + " & ", shell=True)

try:
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((addr, port))
	print("connected!")
except bluetooth.btcommon.BluetoothError as err:
	pass
