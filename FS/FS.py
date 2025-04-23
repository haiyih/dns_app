from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def send_registration(hostname, ip, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))

@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    send_registration(data["hostname"], data["ip"], data["as_ip"], data["as_port"])
    return '', 201

@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    number = request.args.get("number")
    if not number or not number.isdigit():
        return "Invalid input", 400
    n = int(number)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return jsonify({"result": a}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
