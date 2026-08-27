import requests

ZABBIX_URL = "http://zabbix-server/api_jsonrpc.php"
USERNAME = "Admin"
PASSWORD = "zabbix"


def get_token():

    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": USERNAME,
            "password": PASSWORD
        },
        "id": 1
    }

    r = requests.post(ZABBIX_URL, json=payload)
    return r.json()["result"]


def zabbix_api(method, params):

    token = get_token()

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": token,
        "id": 1
    }

    r = requests.post(ZABBIX_URL, json=payload)
    return r.json()


def problem():

    result = zabbix_api(
        "problem.get",
        {
            "output": "extend"
        }
    )

    text = []

    for p in result["result"]:
        text.append(p["name"])

    if not text:
        return "No Problem"

    return "\n".join(text)


def list_vms():

    result = zabbix_api(
        "host.get",
        {
            "output": [
                "host"
            ]
        }
    )

    hosts = []

    for h in result["result"]:
        hosts.append(h["host"])

    return "\n".join(hosts)


def get_hostid(vm_name):

    result = zabbix_api(
        "host.get",
        {
            "filter": {
                "host": [vm_name]
            }
        }
    )

    if not result["result"]:
        return None

    return result["result"][0]["hostid"]


def status(vm_name):

    hostid = get_hostid(vm_name)

    if not hostid:
        return "VM Not Found"

    return f"{vm_name} is UP"


def get_item(vm_name, keyword):

    hostid = get_hostid(vm_name)

    if not hostid:
        return None

    result = zabbix_api(
        "item.get",
        {
            "hostids": hostid,
            "search": {
                "name": keyword
            },
            "output": [
                "name",
                "lastvalue"
            ]
        }
    )

    if not result["result"]:
        return None

    return result["result"][0]["lastvalue"]


def cpu(vm_name):

    value = get_item(vm_name, "CPU")

    return f"{vm_name} CPU = {value}%"


def memory(vm_name):

    value = get_item(vm_name, "Memory")

    return f"{vm_name} Memory = {value}"


def disk(vm_name):

    value = get_item(vm_name, "Disk")

    return f"{vm_name} Disk = {value}"