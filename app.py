import socket, threading, time, streamlit as st

TCP_PORT = 5000
UDP_PORT = 5001

# ── in-process server ────────────────────────────────────────────────────────

def handle_tcp(conn):
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            conn.sendall(b"ACK: " + data)

def _tcp_server(stop):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", TCP_PORT)); s.listen(5); s.settimeout(1)
    while not stop.is_set():
        try:
            c, _ = s.accept()
            threading.Thread(target=handle_tcp, args=(c,), daemon=True).start()
        except socket.timeout:
            pass
    s.close()

def _udp_server(stop):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", UDP_PORT)); s.settimeout(1)
    while not stop.is_set():
        try:
            data, addr = s.recvfrom(4096)
            s.sendto(b"ACK: " + data, addr)
        except socket.timeout:
            pass
    s.close()

def start_server():
    stop = threading.Event()
    threading.Thread(target=_tcp_server, args=(stop,), daemon=True).start()
    threading.Thread(target=_udp_server, args=(stop,), daemon=True).start()
    return stop

# ── diagnostic tests ─────────────────────────────────────────────────────────

def tcp_test(host, count=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(3)
    try:
        t = time.perf_counter(); s.connect((host, TCP_PORT))
        connect_ms = (time.perf_counter() - t) * 1000
        ok = 0; total = 0
        for i in range(count):
            t = time.perf_counter()
            s.sendall(f"TCP_TEST_{i+1}".encode())
            data = s.recv(4096)
            total += (time.perf_counter() - t) * 1000
            ok += bool(data)
        return {"status": "PASS" if ok == count else "FAIL",
                "sent": count, "received": ok,
                "connect_ms": round(connect_ms, 2),
                "avg_ms": round(total / count, 2)}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}
    finally:
        s.close()

def udp_test(host, count=100):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(1)
    ok = 0; total = 0
    for i in range(count):
        try:
            t = time.perf_counter()
            s.sendto(f"UDP_TEST_{i+1}".encode(), (host, UDP_PORT))
            data, _ = s.recvfrom(4096)
            total += (time.perf_counter() - t) * 1000
            ok += bool(data)
        except socket.timeout:
            pass
    s.close()
    loss = (count - ok) / count * 100
    return {"status": "PASS" if loss <= 5 else "FAIL",
            "sent": count, "received": ok,
            "loss_pct": round(loss, 2),
            "avg_ms": round(total / ok, 2) if ok else 0}

def port_test(host, port):
    s = socket.socket(); s.settimeout(2)
    r = s.connect_ex((host, port)); s.close()
    return {"port": port, "status": "OPEN" if r == 0 else "CLOSED"}

# ── helpers ───────────────────────────────────────────────────────────────────

def badge(status):
    color = "green" if status in ("PASS", "OPEN") else "red"
    return f":{color}[**{status}**]"

# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="NetPulse - Network Diagnostic Tool", page_icon="🌐", layout="centered")
st.title("🌐 NetPulse - Network Diagnostic Tool")

# session state
if "server_stop" not in st.session_state:
    st.session_state.server_stop = None

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    host = st.text_input("Server IP", value="127.0.0.1")
    tcp_count = st.slider("TCP messages", 1, 50, 10)
    udp_count = st.slider("UDP packets", 10, 500, 100)

    st.divider()
    st.subheader("🖥️ Local Server")
    running = st.session_state.server_stop is not None
    if not running:
        if st.button("▶ Start Server", use_container_width=True, type="primary"):
            st.session_state.server_stop = start_server()
            st.rerun()
    else:
        st.success("Server is running")
        if st.button("⏹ Stop Server", use_container_width=True):
            st.session_state.server_stop.set()
            st.session_state.server_stop = None
            st.rerun()

# ── main area ─────────────────────────────────────────────────────────────────
st.subheader("🧪 Run Diagnostics")

col1, col2, col3, col4 = st.columns(4)
run_tcp  = col1.button("TCP Test",  use_container_width=True)
run_udp  = col2.button("UDP Test",  use_container_width=True)
run_port = col3.button("Port Test", use_container_width=True)
run_all  = col4.button("Run All ▶", use_container_width=True, type="primary")

# ── TCP ───────────────────────────────────────────────────────────────────────
if run_tcp or run_all:
    with st.spinner("Running TCP test…"):
        r = tcp_test(host, tcp_count)
    st.subheader(f"TCP Result  {badge(r['status'])}")
    if "error" in r:
        st.error(r["error"])
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sent",        r["sent"])
        c2.metric("Received",    r["received"])
        c3.metric("Connect",     f"{r['connect_ms']} ms")
        c4.metric("Avg Response",f"{r['avg_ms']} ms")

# ── UDP ───────────────────────────────────────────────────────────────────────
if run_udp or run_all:
    with st.spinner("Running UDP test…"):
        r = udp_test(host, udp_count)
    st.subheader(f"UDP Result  {badge(r['status'])}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sent",        r["sent"])
    c2.metric("Received",    r["received"])
    c3.metric("Packet Loss", f"{r['loss_pct']}%")
    c4.metric("Avg Response",f"{r['avg_ms']} ms")

# ── Port ──────────────────────────────────────────────────────────────────────
if run_port or run_all:
    with st.spinner("Testing ports…"):
        r5000 = port_test(host, TCP_PORT)
        r5001 = port_test(host, UDP_PORT)
    st.subheader("Port Test Results")
    c1, c2 = st.columns(2)
    c1.metric("Port 5000 (TCP)", r5000["status"])
    c2.metric("Port 5001 (UDP)", r5001["status"])

st.divider()
st.caption("Uses Python standard library only · TCP port 5000 · UDP port 5001")
