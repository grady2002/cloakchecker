from os import system

INTERFACE = "eth0"
LAN_IP_COMMAND = f"echo $(ifconfig {INTERFACE} | grep inet) > tmp"
WAN_IP_COMMAND = "echo $(curl -X GET --silent https://dnsleaktest.com | grep Hello) > tmp"
WAN_LOCATION_COMMAND = "echo $(curl -X GET --silent https://dnsleaktest.com | grep from) > tmp"
MAC_COMMAND = f"echo $(macchanger --show {INTERFACE}) > tmp"

def get_info(command, filter_index):
	required = None
	with open("tmp", "r") as file:
		data = file.read()
		result = str(data).split()
		required = result[filter_index]
	return str(required)
	
def macs () :
	CURRENT = get_info(system(MAC_COMMAND), 2)
	PERMANENT = get_info(system(MAC_COMMAND), 7)
	return [CURRENT, PERMANENT]

def sanitize(string, split_character, filter_index) :
	return string.split(split_character)[filter_index]

try :
	VARS = {
		"lan": get_info(system(LAN_IP_COMMAND), 1),
		"wan": sanitize(get_info(system(WAN_IP_COMMAND), 2), '<', 0),
		"location": sanitize(get_info(system(WAN_LOCATION_COMMAND), 2), '<', 0),
		"current_mac": macs()[0],
		"permanent_mac": macs()[1],
	}
except Exception as e :
	print(f"An error occured : {e}")

def print_all():
		print("\nIP Info")
		print(f"LAN (WiFi) IP : {VARS['lan']}")
		print(f"WAN (Public) IP : {VARS['wan']}")
		print(f"WAN Location (Might be inaccurate) : {VARS['location']}")
		print("\nMAC Info")
		print(f"Current MAC : {VARS['current_mac']}")
		print(f"Permanent (Original) MAC : {VARS['permanent_mac']}")
		if (VARS['current_mac'] == VARS['permanent_mac']) :
			print(f"use 'sudo macchanger --mac=NEW_MAC {INTERFACE}' to change mac address temporarily")

def myipinfo() :
	print_all()
	system("rm tmp")


system("clear")
myipinfo()