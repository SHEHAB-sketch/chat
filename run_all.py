import subprocess
import time
import os
import sys

def cleanup_ports():
    print("Cleaning up old sessions...")
    if os.name == 'nt':
        # Kill processes on port 5000 and 5001
        for port in [5000, 5001]:
            try:
                cmd = f'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :{port} ^| findstr LISTENING\') do taskkill /F /PID %a /T'
                subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except:
                pass

def start_system():
    print("Starting Smart Academic Advisor System...")
    
    # 0. Cleanup
    cleanup_ports()
    time.sleep(1)

    # 1. Start app.py in a new process
    print("Step 1: Starting Backend (app.py) on port 5000...")
    backend_process = subprocess.Popen([sys.executable, "app.py"])
    
    # Wait for server to spin up and verify it's active
    print("Waiting for server to be ready...")
    time.sleep(5)
    
    # 2. Start Cloudflare Tunnel
    print("Step 2: Starting Global Tunnel (Cloudflare)...")
    tunnel_script = "get_cloudflare_link.py"
    if os.path.exists(tunnel_script):
        subprocess.Popen([sys.executable, tunnel_script])
    else:
        print("❌ Error: get_cloudflare_link.py not found!")
        backend_process.terminate()
        return

    print("\nSystem is launching!")
    print("-----------------------------------------")
    print("1. Local Access: http://localhost:5000")
    print("2. Global Access: Check 'Link_For_Friends.txt' shortly.")
    print("-----------------------------------------")
    print("Keep this window open to keep the server running.")
    
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        backend_process.terminate()

if __name__ == "__main__":
    start_system()
