from os import system

INTERFACE = "eth0"
LAN_IP_COMMAND = f"echo $(ifconfig {INTERFACE} | grep inet) > tmp"
WAN_IP_COMMAND = "echo $(curl -X GET --silent https://dnsleaktest.com | grep Hello) > tmp"
WAN_LOCATION_COMMAND = "echo $(curl -X GET --silent https://dnsleaktest.com | grep from) > tmp"
MAC_COMMAND = f"echo $(macchanger --show {INTERFACE}) > tmp"

def get_info(command: str, filter_index: int) -> str:
	required = None
	with open("tmp", "r") as file:
		data = file.read()
		result = str(data).split()
		required = result[filter_index]
	return str(required)
	
def macs () -> list :
	CURRENT = get_info(system(MAC_COMMAND), 2)
	PERMANENT = get_info(system(MAC_COMMAND), 7)
	return [CURRENT, PERMANENT]

def sanitize(string: str, split_character: chr or str, filter_index: int) -> str :
	return string.split(split_character)[filter_index]

try :
	VARS = {
		# "lan": get_info(command=system(LAN_IP_COMMAND), filter_index = 1),
		"wan": sanitize(string=get_info(command=system(WAN_IP_COMMAND), filter_index=2), split_character='<', filter_index=0),
		"location": sanitize(string=get_info(command=system(WAN_LOCATION_COMMAND), filter_index=2), split_character='<', filter_index=0),
		# "current_mac": macs()[0],
		# "permanent_mac": macs()[1],
	}
except Exception as e :
	print(f"An error occured : {e}")

def print_all() -> None:
		# print(f"LAN (WiFi) IP : {VARS['lan']}")
		print(f"WAN (Public) IP : {VARS['wan']}")
		print(f"WAN Location (Might be inaccurate) : {VARS['location']}")
		# print(f"Current MAC : {VARS['current_mac']}")
		# print(f"Permanent (Original) MAC : {VARS['permanent_mac']}")
		# if (VARS['current_mac'] == VARS['permanent_mac']) :
			# print(f"use 'sudo macchanger --mac=NEW_MAC {INTERFACE}' to change mac address temporarily")

def myipinfo() -> None :
	print_all()
	system("rm tmp")


system("clear")
myipinfo()
