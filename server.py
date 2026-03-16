try:
    
    import socket
    import json
    import datetime
    import threading

    # הגדרות שרת
    HOST = '0.0.0.0'
    PORT = 9999

    failed_attempts_tracker = {}
    attempts_lock = threading.Lock()

    def load_users():
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: users.json not found. Please create it.")
            return {}
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}

    def handle_client(conn, addr):
        client_ip = addr[0]
        attemptLimit = 4
        
        with conn:
            print(f"New connection from {addr}")
            try:
                rawDataFromClient = conn.recv(1024)
                if not rawDataFromClient:
                    return
                
                dataFromClient = rawDataFromClient.decode('utf-8').strip()

                if dataFromClient.startswith("login|"):
                    parts = dataFromClient.split("|")
                    if len(parts) < 3:
                        conn.sendall("400 bad request".encode('utf-8'))
                        return

                    username = parts[1]
                    password = parts[2]
                    
                    with attempts_lock:
                        current_attempts = failed_attempts_tracker.get(client_ip, 0)
                    
                    if current_attempts >= attemptLimit:
                        conn.sendall("attempt limit reached".encode("utf-8"))
                        print(f"Blocked login attempt from {client_ip} (Limit reached)")
                        return

                    users = load_users()
                    if username in users and users[username] == password:
                        conn.sendall("200 ok".encode('utf-8'))
                        status = "success"

                        with attempts_lock:
                            failed_attempts_tracker[client_ip] = 0
                    else:
                        conn.sendall("401 unauthorized".encode('utf-8'))
                        status = "failed"

                        with attempts_lock:
                            failed_attempts_tracker[client_ip] = failed_attempts_tracker.get(client_ip, 0) + 1
                            print(f"Failed attempt {failed_attempts_tracker[client_ip]} from {client_ip}")

                    with open("server_connection_logs.json", "a", encoding="utf-8") as f:
                        logFields = {
                            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "address": str(addr),
                            "username": username,
                            "status": status
                        }
                        f.write(json.dumps(logFields, ensure_ascii=False) + "\n")

                elif dataFromClient == "freer premition":
                    conn.sendall("200 ok".encode('utf-8'))

            except Exception as e:
                print(f"Error handling client {addr}: {e}")

    def start_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server is listening on port {PORT} (Multi-threaded & Attempt Tracker)...")
            
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()

    if __name__ == "__main__":
        start_server()
        
except KeyboardInterrupt:
    print("KeyboardInterrupt! QUITING...")