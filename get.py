import socket
import requests

# 獲取公共 IP 地址
def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

# 獲取私有 IP 地址
def get_private_ip():
    # 建立一個 UDP socket，並連接到一個公共網址
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    # 獲取本機 IP 地址
    private_ip = sock.getsockname()[0]
    sock.close()
    return private_ip

if __name__ == '__main__':
    print(f"Public IP: {get_public_ip()}")
    print(f"Private IP: {get_private_ip()}")
