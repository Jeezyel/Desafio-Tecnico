# netbox_integration.py  (ou junte ao seu main.py)
import requests
import ipaddress
from typing import Optional

# NETBOX_API_URL = os.getenv("NETBOX_API_URL", "http://192.168.10.114:8000/api")
# NETBOX_API_TOKEN = os.getenv("NETBOX_API_TOKEN", "e15cada4fc7f10c7f7e85d957dc55fcd043afffe")  

#HEADERS = {
#    "Authorization": f"Token {NETBOX_API_TOKEN}" if NETBOX_API_TOKEN else "",
#    "Content-Type": "application/json",
#    "Accept": "application/json",
#}

HEADERS = {"Authorization" : "Token e15cada4fc7f10c7f7e85d957dc55fcd043afffe"}
url = "http://192.168.10.114:8000/api"

REQUEST_TIMEOUT = 40


# ---- HTTP helpers ----
def nb_get(path: str, params: dict = None):
    url = "http://192.168.10.114:8000/api/dcim/devices"
    resp = requests.get(url, headers=HEADERS, verify=False, timeout=REQUEST_TIMEOUT, params=params)
    resp.raise_for_status()
    return resp.json()


def nb_post(path: str, payload: dict):
    url = "http://192.168.10.114:8000/api/dcim/devices"
    resp = requests.post(url, headers=HEADERS, json=payload, verify=False, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def nb_patch(path: str, payload: dict):
    url = f"{NETBOX_API_URL.rstrip('/')}/{path.lstrip('/')}"
    resp = requests.patch(url, headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


# ---- Utility ----
def netmask_to_prefix(netmask: str) -> int:
    # Ex: 255.255.255.0 -> 24
    return ipaddress.IPv4Network(f"0.0.0.0/{netmask}").prefixlen


# ---- Ensure resources (site, manufacturer, device type, device role) ----
def ensure_site(site_name: str) -> int:
    if not site_name:
        site_name = "default"
    r = nb_get("dcim/sites/", params={"name": site_name})
    if r["count"] > 0:
        return r["results"][0]["id"]
    payload = {"name": site_name, "slug": site_name.replace(" ", "-").lower()}
    created = nb_post("dcim/sites/", payload)
    return created["id"]


def ensure_manufacturer(manufacturer_name: str) -> int:
    if not manufacturer_name:
        manufacturer_name = "Generic"
    r = nb_get("dcim/manufacturers/", params={"name": manufacturer_name})
    if r["count"] > 0:
        return r["results"][0]["id"]
    created = nb_post("dcim/manufacturers/", {"name": manufacturer_name, "slug": manufacturer_name.replace(" ", "-").lower()})
    return created["id"]


def ensure_device_type(manufacturer_id: int, model_name: str) -> int:
    # Search by model and manufacturer
    params = {"model": model_name, "manufacturer_id": manufacturer_id}
    r = nb_get("dcim/device-types/", params=params)
    if r["count"] > 0:
        return r["results"][0]["id"]
    payload = {"manufacturer": manufacturer_id, "model": model_name, "slug": model_name.replace(" ", "-").lower()}
    created = nb_post("dcim/device-types/", payload)
    return created["id"]


def ensure_device_role(role_name: str = "Network Device") -> int:
    if not role_name:
        role_name = "Network Device"
    r = nb_get("dcim/device-roles/", params={"name": role_name})
    if r["count"] > 0:
        return r["results"][0]["id"]
    payload = {"name": role_name, "slug": role_name.replace(" ", "-").lower()}
    created = nb_post("dcim/device-roles/", payload)
    return created["id"]


# ---- Device operations ----
def get_device_by_name(name: str) -> Optional[dict]:
    r = nb_get("dcim/devices/", params={"name": name})
    if r["count"] > 0:
        return r["results"][0]
    return None


def create_device(name: str, site_id: int, device_type_id: int, device_role_id: int, description: str = "") -> dict:
    payload = {
        "name": name,
        "device_type": device_type_id,
        "device_role": device_role_id,
        "site": site_id,
        "comments": description
    }
    return nb_post("dcim/devices/", payload)


def update_device(device_id: int, update_fields: dict) -> dict:
    return nb_patch(f"dcim/devices/{device_id}/", update_fields)


# ---- Interfaces ----
def get_interface(device_id: int, name: str) -> Optional[dict]:
    r = nb_get("dcim/interfaces/", params={"device_id": device_id, "name": name})
    if r["count"] > 0:
        return r["results"][0]
    return None


def create_interface(device_id: int, name: str, mac_address: Optional[str], mtu: Optional[int] = None) -> dict:
    payload = {"device": device_id, "name": name}
    if mac_address:
        payload["mac_address"] = mac_address
    if mtu:
        payload["mtu"] = mtu
    return nb_post("dcim/interfaces/", payload)


# ---- IP Addresses ----
def get_ip_address(address_cidr: str) -> Optional[dict]:
    r = nb_get("ipam/ip-addresses/", params={"address": address_cidr})
    if r["count"] > 0:
        return r["results"][0]
    return None


def create_ip_address(address_cidr: str, interface_id: int) -> dict:
    payload = {"address": address_cidr, "assigned_object_type": "dcim.interface", "assigned_object_id": interface_id}
    return nb_post("ipam/ip-addresses/", payload)


# ---- High-level orchestration for a device from your SNMP JSON ----
def sync_device_to_netbox(snmp_device: dict) -> dict:
    """
    snmp_device is one entry from your JSON (e.g. the value of key "192.168.1.1").
    Expected keys used: sysName, sysDescr, sysLocation, interfaces (list)
    """
    summary = {"device": snmp_device.get("sysName"), "actions": [], "errors": []}

    try:
        site_name = snmp_device.get("sysLocation") or "default"
        site_id = ensure_site(site_name)

        # try to derive manufacturer and model from sysDescr or sysObjectID
        # simple heuristic: manufacturer = first token of sysDescr
        sys_descr = snmp_device.get("sysDescr") or ""
        manufacturer_name = sys_descr.split()[0] if sys_descr else "Generic"
        model_name = snmp_device.get("sysName") or "unknown-model"

        manufacturer_id = ensure_manufacturer(manufacturer_name)
        device_type_id = ensure_device_type(manufacturer_id, model_name)
        device_role_id = ensure_device_role("Network Device")

        device = get_device_by_name(snmp_device.get("sysName"))
        if device:
            # update basic fields (idempotent)
            device_id = device["id"]
            update_payload = {"comments": sys_descr, "site": site_id}
            update_device(device_id, update_payload)
            summary["actions"].append(f"updated device {device['name']} (id {device_id})")
        else:
            created = create_device(snmp_device.get("sysName"), site_id, device_type_id, device_role_id, description=sys_descr)
            device_id = created["id"]
            summary["actions"].append(f"created device {created['name']} (id {device_id})")

        # Interfaces
        for intf in snmp_device.get("interfaces", []):
            intf_name = intf.get("ifDescr") or f"if{intf.get('ifIndex')}"
            mac = intf.get("ifPhysAddress")
            existing_intf = get_interface(device_id, intf_name)
            if existing_intf:
                intf_id = existing_intf["id"]
                summary["actions"].append(f"interface exists: {intf_name} (id {intf_id})")
            else:
                created_if = create_interface(device_id, intf_name, mac)
                intf_id = created_if["id"]
                summary["actions"].append(f"created interface {intf_name} (id {intf_id})")

            # If interface has IP, create ipam entry
            ipaddr = intf.get("ipAddress")
            netmask = intf.get("ipNetmask")
            if ipaddr and netmask:
                prefix = netmask_to_prefix(netmask)
                cidr = f"{ipaddr}/{prefix}"
                existing_ip = get_ip_address(cidr)
                if existing_ip:
                    summary["actions"].append(f"ip exists: {cidr}")
                else:
                    create_ip_address(cidr, intf_id)
                    summary["actions"].append(f"created ip {cidr} on interface {intf_name}")

    except requests.HTTPError as e:
        summary["errors"].append(f"HTTPError: {str(e)}")
    except Exception as e:
        summary["errors"].append(f"Exception: {str(e)}")

    return summary
