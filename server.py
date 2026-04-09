try:
    
    import ssl
    import socket
    import json
    import datetime
    import threading
    import hashingAlg

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
            print(f"[+] New connection from {addr}")
            try:
                rawDataFromClient = conn.recv(1024)
                print("[+] handeling client")
                print("[+] listenning")
                if not rawDataFromClient:
                    return
                
                dataFromClient = rawDataFromClient.decode('utf-8').strip()
                if dataFromClient.startswith("login|") or dataFromClient.startswith("signUp|"):
                    print("[+] recived sensetive data. can not show info") 
                
                else:
                    print(f"[+] subject recived: {dataFromClient} | ({addr})") 

                if dataFromClient.startswith("login|"):
                    parts = dataFromClient.split("|")
                    if len(parts) < 3:
                        print(f"[+] sending '400 bad request' to client: {addr}")
                        conn.sendall("400 bad request".encode('utf-8'))
                        print(f"[+] sent.")
                        return

                    username = parts[1]
                    passwordFromClient = parts[2]
                    
                    with attempts_lock:
                        current_attempts = failed_attempts_tracker.get(client_ip, 0)
                    
                    if current_attempts >= attemptLimit:
                        conn.sendall("attempt limit reached".encode("utf-8"))
                        print(f"[+] Blocked login attempt from {client_ip} (Limit reached)")
                        return

                    print("[+] loading users")
                    users = load_users()
                    print("[+] successfuly loaded users")
                    if username in users:
                        userData = users[username]
                        storedPassword = userData["password"]
                        salt_hex, stored_hash_hex = storedPassword.split(":")
                        salt = bytes.fromhex(salt_hex)
                        stored_hash = bytes.fromhex(stored_hash_hex)
                        
                        if hashingAlg.verify_password(salt, stored_hash, passwordFromClient):
                            print(f"[+] sending '200 ok' to client: {addr}")
                            conn.sendall("200 ok".encode('utf-8'))
                            print("[+] sent.")
                            status = "success"
                            with attempts_lock:
                                failed_attempts_tracker[client_ip] = 0
                        
                        else:
                            print(f"[+] sending '401 unauthorized' to client: {addr}")
                            conn.sendall("401 unauthorized".encode('utf-8'))
                            print("[+] sent.")
                            status = "failed"            
                        
                    else:
                        print(f"[+] sending '401 unauthorized' to client: {addr}")
                        conn.sendall("401 unauthorized".encode('utf-8'))
                        print("[+] sent.")
                        status = "failed"

                        with attempts_lock:
                            failed_attempts_tracker[client_ip] = failed_attempts_tracker.get(client_ip, 0) + 1
                            print(f"[+] Failed attempt {failed_attempts_tracker[client_ip]} from {client_ip}")

                    with open("server_connection_logs.json", "a", encoding="utf-8") as f:
                        logFields = {
                            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "address": str(addr),
                            "username": username,
                            "status": status
                        }
                        
                        print(f"[+] writing a connection log for client: {addr}")
                        f.write(json.dumps(logFields, ensure_ascii=False) + "\n")
                        print("[+] completed writing the connection log.")

                elif dataFromClient == "freer premition":
                    print(f"[+] sending '200 ok' to client: {addr}")
                    conn.sendall("200 ok".encode('utf-8'))
                    print("[+] sent.")
                
                elif dataFromClient.startswith("get_schedule|"):
                    class_name = dataFromClient.split("|")[1]
                    try:
                        with open("schedule.json", "r", encoding="utf-8") as f:
                            schedules = json.load(f)
                            class_schedule = schedules.get(class_name, {})
                            conn.sendall(json.dumps(class_schedule, ensure_ascii=False).encode('utf-8'))
                    except FileNotFoundError:
                        conn.sendall("error|file not found".encode('utf-8'))
                
                elif dataFromClient.startswith("signUp|"):
                    parts = dataFromClient.split("|")
                    if len(parts) != 6:
                        print(f"[+] sending '400 bad request' to client: {addr}")
                        conn.sendall("400 bad request".encode('utf-8'))
                        print(f"[+] sent.")
                        return

                    print("[+] analizing the data")
                    firstName = parts[1]
                    lastName = parts[2]
                    gmail = parts[3]
                    newUsername = parts[4]
                    newPassword = parts[5]
                    timeCreated = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    print("[+] opening users.json")
                    with open("users.json", "r", encoding='utf-8') as f:
                        users = json.load(f)
                        
                        for username, data in users.items():
                            if data["gmail_account"] == gmail:
                                print(f"[+] found email for user: {username}")
                                conn.sendall("gmail already exists".encode('utf-8'))
                                return

                        if newUsername in users:
                            print("[+] found that username is in use")
                            conn.sendall("username already exists".encode('utf-8'))
                            return
                        
                    salt, hashed_tuple = hashingAlg.hash_new_password(newPassword)
                    password_to_save = f"{salt.hex()}:{hashed_tuple.hex()}"
                    
                    users[newUsername] = {
                        "id": len(users) + 1,
                        "password": password_to_save,
                        "first_name": firstName,
                        "last_name": lastName,
                        "gmail_account": gmail,
                        "created_at": timeCreated
                    }
                    
                    with open("users.json", "w", encoding='utf-8') as f:
                        print("[+] appending new user")
                        json.dump(users, f, indent=4)
                        print("[+] successfuly appended new user") 
                    
                        conn.sendall("200 ok".encode('utf-8'))            
                    
            except ValueError as e:
                print(f"[+] Error handling client {addr}: {e}")

    def start_server():
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("server.crt", "server.key")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"[+] Server is listening on port: '{PORT}'")
            with context.wrap_socket(s, server_side=True) as ss:
                while True:
                    conn, addr = ss.accept()
                    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                    client_thread.start()

    if __name__ == "__main__":
        start_server()
        
except KeyboardInterrupt:
    print("[+] KeyboardInterrupt! QUITING...")