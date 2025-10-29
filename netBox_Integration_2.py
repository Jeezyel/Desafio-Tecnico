
# codigo mais simples para teste de conexao com a API do NetBox
import requests
from rich import print as r_print

HEADERS = {"Authorization" : "Token e15cada4fc7f10c7f7e85d957dc55fcd043afffe"}

REQUEST_TIMEOUT = 40

reponse = requests.get("http://192.168.10.114:8000/api/dcim/devices", headers=HEADERS, verify=False)
r_print(reponse.json())