from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

def query_dns(as_ip, as_port, hostname):
    query = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query.encode(), (as_ip, int(as_port)))
    data, _ = sock.recvfrom(1024)
    response = dict(line.split("=", 1) for line in data.decode().split("\n") if "=" in line)
    return response.get("VALUE")

@app.route("/fibonacci", methods=["GET"])
def fibonacci_request():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Missing parameters", 400

    try:
        fs_ip = query_dns(as_ip, as_port, hostname)
        if not fs_ip:
            return "DNS resolution failed", 400

        response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": number})
        return (response.content, response.status_code)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
