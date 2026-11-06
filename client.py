import socket,time

def tcp_test(host,port=5000,count=10):
    print('\n=== TCP TEST ==='); s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(3)
    try:
        t=time.perf_counter(); s.connect((host,port)); connect=(time.perf_counter()-t)*1000; ok=0; total=0
        for i in range(count):
            t=time.perf_counter(); s.sendall(f'TCP_TEST_{i+1}'.encode()); data=s.recv(4096); total+=(time.perf_counter()-t)*1000; ok+=bool(data)
        print(f'Connection: SUCCESS\nMessages sent: {count}\nMessages received: {ok}\nConnection time: {connect:.2f} ms\nAverage response: {total/count:.2f} ms\nResult: {"PASS" if ok==count else "FAIL"}')
    except Exception as e: print('Connection: FAILED\nReason:',e)
    finally: s.close()

def udp_test(host,port=5001,count=100):
    print('\n=== UDP TEST ==='); s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.settimeout(1); ok=0; total=0
    for i in range(count):
        try:
            t=time.perf_counter(); s.sendto(f'UDP_TEST_{i+1}'.encode(),(host,port)); data,_=s.recvfrom(4096); total+=(time.perf_counter()-t)*1000; ok+=bool(data)
        except socket.timeout: pass
    s.close(); loss=(count-ok)/count*100; print(f'Packets sent: {count}\nPackets received: {ok}\nPacket loss: {loss:.2f}%\nAverage response: {(total/ok if ok else 0):.2f} ms\nResult: {"PASS" if loss<=5 else "FAIL"}')

def port_test(host,port):
    print('\n=== PORT TEST ==='); s=socket.socket(); s.settimeout(2); r=s.connect_ex((host,port)); print('Port status:', 'OPEN' if r==0 else 'CLOSED / UNREACHABLE'); s.close()

print('=== NetPulse Network Diagnostic Tool ===')
host=input('Server IP [127.0.0.1]: ').strip() or '127.0.0.1'
print('\n1. TCP test\n2. UDP test\n3. Port test\n4. Run all tests'); choice=input('Choose: ').strip()
if choice=='1': tcp_test(host)
elif choice=='2': udp_test(host)
elif choice=='3': port_test(host,int(input('Port [5000]: ') or '5000'))
elif choice=='4': tcp_test(host); udp_test(host); port_test(host,5000)
else: print('Invalid option')
