# NetPulse 🌐

**NetPulse** is a lightweight, real-time TCP & UDP network diagnostic and benchmarking tool. It provides both an interactive **Streamlit web dashboard** and high-performance **CLI tools** to analyze network latency, packet loss, port reachability, and client-server communication behavior.

Built strictly using Python's standard library (`socket`, `threading`, and `time`) for the core networking engine, NetPulse requires no heavy network dependencies.

---

## 🚀 Features

- **TCP Latency & Response Benchmark**:
  - Measures connection handshake time (`connect_ms`).
  - Benchmarks sequential round-trip echo response times.
  - Validates full payload delivery and acknowledgment.
- **UDP Packet Loss & Jitter Test**:
  - High-speed datagram burst testing.
  - Calculates exact packet loss percentage (`loss_pct`).
  - Computes average round-trip latency for received packets.
- **Port Reachability Testing**:
  - Quick socket probe to check open vs. closed/filtered ports.
- **Interactive Streamlit Web Dashboard**:
  - In-process server control (Start/Stop server directly from the UI).
  - Configurable message and packet counts via sliders.
  - Color-coded metrics and test result badges (PASS/FAIL/OPEN/CLOSED).
- **Standalone CLI Tools & Batch Scripts**:
  - Dedicated CLI server (`server.py`) and client (`client.py`).
  - Quick-launch Windows `.bat` scripts (`run_app.bat`, `run_server.bat`, `run_client.bat`).

---

## 📁 Project Structure

```text
NetPulse/
│
├── app.py              # Streamlit Web UI & in-process server/diagnostic runner
├── client.py           # CLI diagnostic client
├── server.py           # Standalone multi-threaded TCP/UDP echo server
│
├── run_app.bat         # Windows launcher for Streamlit Web UI
├── run_server.bat      # Windows launcher for CLI server
├── run_client.bat      # Windows launcher for CLI client
│
├── requirements.txt    # Project dependencies (streamlit)
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.10+** installed.
- Ensure `python` and `pip` are added to your system PATH.

### 1. Clone the Repository
```bash
git clone https://github.com/ThanuSuthapalli/NetPulse.git
cd NetPulse
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Usage

### Option 1: Streamlit Web Dashboard (Recommended)

Run the web app via terminal:
```bash
streamlit run app.py
```
*Or on Windows, simply double-click `run_app.bat`.*

1. Open your browser at `http://localhost:8501`.
2. In the sidebar, click **▶ Start Server** (if running locally) or specify a remote Server IP.
3. Choose **TCP Test**, **UDP Test**, **Port Test**, or click **Run All ▶**.
4. View metrics, packet loss rates, and response times in real time.

---

### Option 2: CLI Client & Server

#### 1. Start the Server
In a terminal:
```bash
python server.py
```
*Or double-click `run_server.bat`.*
The server listens for:
- **TCP**: Port `5000`
- **UDP**: Port `5001`

#### 2. Run the Client
In a second terminal:
```bash
python client.py
```
*Or double-click `run_client.bat`.*

Select an option from the menu:
- `1` - TCP test (latency & round-trip time)
- `2` - UDP test (packet loss & latency)
- `3` - Port test (checks port status)
- `4` - Run all tests

---

## 🌐 Network Testing Configurations

### Local Testing (Same Machine)
- Target IP: `127.0.0.1` (localhost).

### LAN / Two-PC Testing
1. On the **Server machine**, find its local IPv4 address:
   - **Windows**: Run `ipconfig` in Command Prompt.
   - **macOS / Linux**: Run `ifconfig` or `ip a`.
2. Ensure the firewall permits inbound traffic on ports **5000 (TCP)** and **5001 (UDP)**:
   - On Windows, allow Python through the Windows Defender Firewall for Private Networks when prompted.
3. On the **Client machine**, launch `client.py` or `app.py` and enter the server's IPv4 address.

---

## 🧠 Concepts Demonstrated

| Concept | Explanation in NetPulse |
| :--- | :--- |
| **TCP (SOCK_STREAM)** | Connection-oriented, guarantees delivery and ordering via ACKs. NetPulse measures handshake time and per-message latency. |
| **UDP (SOCK_DGRAM)** | Connectionless, fire-and-forget. Used for speed-sensitive applications; NetPulse quantifies packet loss under burst conditions. |
| **Multi-threading** | Server spawns worker threads per connection (`threading.Thread`) to handle concurrent clients without blocking. |
| **Socket Polling & Timeouts** | Sockets use timeouts to detect dropped packets or unreachable hosts without hanging indefinitely. |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) or standard open-source terms. Contributions and feedback are welcome!
