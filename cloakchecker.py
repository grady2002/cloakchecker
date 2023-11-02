from os import system
from json import loads

INTERFACE = "eth0"
LAN_IP_COMMAND = f"echo $(ifconfig {INTERFACE} | grep inet) > tmp.info"
WAN_IP_COMMAND = "echo $(curl -X GET --silent https://dnsleaktest.com | grep Hello) > tmp.info"
MAC_COMMAND = f"echo $(macchanger --show {INTERFACE}) > tmp.info"

def get_info(command: str, filter_index: int) -> str:
	required = None
	with open("tmp.info", "r") as file:
		data = file.read()
		result = str(data).split()
		required = result[filter_index]
		file.close()
	system("rm tmp.info")
	return str(required)

def get_wan_location() -> dict :
    location = {}
    ip = sanitize(string=get_info(command=system(WAN_IP_COMMAND), filter_index=2), split_character='<', filter_index=0)
    system(f"curl -X GET --silent http://ip-api.com/json/{ip} > loc.info")
    with open("loc.info", "r") as file :
        data = loads(file.read())
        location = {
			'city': data['city'],
			'country': data['country']
		}
        file.close()
    system("rm loc.info")
    return location
	
def macs () -> list :
	CURRENT = get_info(system(MAC_COMMAND), 2)
	PERMANENT = get_info(system(MAC_COMMAND), 7)
	return [CURRENT, PERMANENT]

def sanitize(string: str, split_character: chr or str, filter_index: int) -> str :
	return string.split(split_character)[filter_index]

VARS = {
	# "lan": get_info(command=system(LAN_IP_COMMAND), filter_index = 1),
	"wan": sanitize(string=get_info(command=system(WAN_IP_COMMAND), filter_index=2), split_character='<', filter_index=0),
	"location": f"{get_wan_location()['city']}, {get_wan_location()['country']}" 
	# "current_mac": macs()[0],
	# "permanent_mac": macs()[1],
}

def myipinfo() -> None :
    system("clear")
    for key, value in VARS.items() :
        print(f"{key} : {value}")

myipinfo()