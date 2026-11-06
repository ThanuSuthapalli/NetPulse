import socket, threading, time
HOST='0.0.0.0'; TCP_PORT=5000; UDP_PORT=5001

def handle_tcp(conn, addr):
    with conn:
        while True:
            data=conn.recv(4096)
            if not data: break
            conn.sendall(b'ACK: '+data)

def tcp_server():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind((HOST,TCP_PORT)); s.listen(5)
    print(f'[TCP SERVER] Listening on {TCP_PORT}')
    while True:
        c,a=s.accept(); print('[TCP] Connected:',a); threading.Thread(target=handle_tcp,args=(c,a),daemon=True).start()

def udp_server():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind((HOST,UDP_PORT)); print(f'[UDP SERVER] Listening on {UDP_PORT}')
    while True:
        data,a=s.recvfrom(4096); s.sendto(b'ACK: '+data,a)

threading.Thread(target=tcp_server,daemon=True).start(); threading.Thread(target=udp_server,daemon=True).start()
print('NetPulse Network Communication Server running. Ctrl+C to stop.')
try:
    while True: time.sleep(1)
except KeyboardInterrupt: print('Stopped.')
