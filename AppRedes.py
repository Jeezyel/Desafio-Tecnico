from flask import Flask, jsonify, request
import json
import os
from netbox_integration import sync_device_to_netbox   # IMPORTANTE

app = Flask(__name__)

DB_PATH = "simulated_snmp_data.json"


def ler_snmp_simulado():
    """Lê o arquivo JSON com os dados simulados de dispositivos."""
    if not os.path.exists(DB_PATH):
        return {}

    with open(DB_PATH, "r") as f:
        return json.load(f)


@app.route("/api/v1/discover", methods=["POST"])
def discover():
    body = request.get_json()

    # Validação do corpo da requisição
    if not body or "ips" not in body:
        return jsonify({
            "erro": "Envie o JSON no formato: { 'ips': ['192.168.1.1', '192.168.1.2'] }"
        }), 400

    ips = body["ips"]

    if not isinstance(ips, list) or len(ips) == 0:
        return jsonify({"erro": "'ips' deve ser uma lista com pelo menos 1 IP"}), 400

    dados_snmp = ler_snmp_simulado()
    resposta = []

    # Para cada IP solicitado, busca no JSON
    for ip in ips:
        if ip in dados_snmp:

            # Chama o NetBox para criar/atualizar device, interfaces, IPs
            sync_result = sync_device_to_netbox(dados_snmp[ip])

            resposta.append({
                "ip": ip,
                "device": dados_snmp[ip]["sysName"],
                "resultado_netbox": sync_result,   
                "resultado_json": dados_snmp[ip]
            })
        else:
            resposta.append({
                "ip": ip,
                "erro": "Nenhum dispositivo encontrado neste IP"
            })

    return jsonify({
        "mensagem": "Descoberta concluída!",
        "dispositivos": resposta
    }), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API funcionando!"}), 200


@app.route("/All", methods=["GET"])
def All():
    All_Data = ler_snmp_simulado()
    return jsonify(All_Data), 200


if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)
