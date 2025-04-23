import socket

dns_records = {}

UDP_IP = "0.0.0.0"
UDP_PORT = 53533

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Authoritative Server listening on port 53533...")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode().strip().split("\n")
    fields = dict(line.split("=", 1) for line in message if "=" in line)

    if "TTL" in fields:  # Registration
        dns_records[fields["NAME"]] = (fields["VALUE"], fields["TYPE"], fields["TTL"])
        print(f"Registered {fields['NAME']} with IP {fields['VALUE']}")
    elif "TYPE" in fields and "NAME" in fields:  # DNS Query
        name = fields["NAME"]
        if name in dns_records:
            ip, typ, ttl = dns_records[name]
            response = f"TYPE={typ}\nNAME={name}\nVALUE={ip}\nTTL={ttl}\n"
            sock.sendto(response.encode(), addr)
