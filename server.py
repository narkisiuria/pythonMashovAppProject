try:
    import os
    import ssl
    import socket
    import json
    import datetime
    import threading
    from utils import hashingAlg

    print(os.getcwd())

    class Server:
        def __init__(self, host='0.0.0.0', port=9999):
            self.host = host
            self.port = port
            self.failed_attempts_tracker = {}
            self.attempts_lock = threading.Lock()
            self.db_lock = threading.Lock() 
            self.attempt_limit = 4

        def load_users(self):
            with self.db_lock:
                try:
                    print("[+] oppening data/users.json and reading it")
                    with open("data/users.json", "r", encoding="utf-8") as f:
                        print("[+] oppend data/users.json")
                        print("[+] returing the data of users")
                        return json.load(f)
                    
                except FileNotFoundError:
                    print("Error: data/users.json not found. Please create it.")
                    return {}
                
                except Exception as e:
                    print(f"Error loading users: {e}")
                    return {}

        def log_connection(self, addr, username, status):
            with self.db_lock:
                print("[+] oppening data/server_connection_logs.json")
                with open("data/server_connection_logs.json", "a", encoding="utf-8") as f:
                    print("[+] successfuly oppend data/server_connection_logs.json")
                    log_fields = {
                        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "address": str(addr),
                        "username": username,
                        "status": status
                    }
                    
                    print(f"[+] writing a connection log for client: {addr}")
                    f.write(json.dumps(log_fields, ensure_ascii=False) + "\n")
                    print("[+] completed writing the connection log.")

        def handle_login(self, conn, addr, dataFromClient):
            print("[+] handling log in")
            client_ip = addr[0]
            parts = dataFromClient.split("|")
            
            if len(parts) < 3:
                print(f"[+] sending '400 bad request' to client: {addr}")
                conn.sendall("400 bad request".encode('utf-8'))
                return

            print("[+] getting username + password from client")
            username = parts[1]
            passwordFromClient = parts[2]
            print("[+] successfuly got the username + password from the client")
            
            with self.attempts_lock:
                current_attempts = self.failed_attempts_tracker.get(client_ip, 0)
            
            if current_attempts >= self.attempt_limit:
                print("[*] attempt limit reached detected!")
                print("[*] blocking attemptor")
                conn.sendall("attempt limit reached".encode("utf-8"))
                print(f"[+] successfuly blocked login attempt from client: {client_ip} hint: (Limit reached)")
                return

            print("[+] loading users")
            users = self.load_users()
            print("[+] successfully loaded users")
            
            status = "failed"
            if username in users:
                print("[+] username is in users")
                print("[+] collecting user's data")
                userData = users[username]
                storedPassword = userData.get("password", "")
                print("[+] suucessfuly collected user's data")
                
                if ":" in storedPassword:
                    print("[+] found that ':' is in user's data")
                    salt_hex, stored_hash_hex = storedPassword.split(":")
                    salt = bytes.fromhex(salt_hex)
                    stored_hash = bytes.fromhex(stored_hash_hex)
                    
                    if hashingAlg.verify_password(salt, stored_hash, passwordFromClient):
                        print("[+] login suuccesful")
                        print(f"[+] sending '200 ok' to client: {addr}")
                        print("[+] getting user's role")
                        role = userData.get("role", "student") 
                        print("[+] getting user's class name")
                        class_name = userData.get("class", "unknown")
                        print("[+] sending client his role|class name")
                        conn.sendall(f"200 ok|{role}|{class_name}".encode("utf-8"))
                        print("[+] successfuly sent client his role|class name")
                        print["[*] status is success"]
                        status = "success"
                        
                        with self.attempts_lock:
                            self.failed_attempts_tracker[client_ip] = 0
                    else:
                        self._send_unauthorized(conn, addr, client_ip)
                else:
                    self._send_unauthorized(conn, addr, client_ip)
            else:
                self._send_unauthorized(conn, addr, client_ip)

            self.log_connection(addr, username, status)

        def _send_unauthorized(self, conn, addr, client_ip):
            print(f"[+] sending '401 unauthorized' to client: {addr}")
            conn.sendall("401 unauthorized".encode('utf-8'))
            print(f"[+] suuccessfuly sent 401 unauthorized to client: {addr}")
            with self.attempts_lock:
                print("[+] updating attempts lock")
                self.failed_attempts_tracker[client_ip] = self.failed_attempts_tracker.get(client_ip, 0) + 1
                print("[+] geting faild attempt")
                print(f"[+] Failed attempt {self.failed_attempts_tracker[client_ip]} from {client_ip}")

        def handle_signup(self, conn, addr, dataFromClient):
            parts = dataFromClient.split("|")
            if len(parts) != 9:
                print("[*] found that the length of the request from the client is not equle to 9")
                print(f"[+] sending '400 bad request' to client: {addr}. hint: (check length of request)")
                conn.sendall("400 bad request".encode('utf-8'))
                print(f"successfuly sent 400 bad request to client: {addr}")
                return

            print("[+] analyzing the data")
            firstName, lastName, gmail, newUsername, newPassword = parts[1:6]
            print(f"[+] done analyzing the data of user: {addr}")
            
            print("[+] getting class map")
            class_map = {
                "ט1": "9th1", "ט2": "9th2", "ט3": "9th3",
                "ט4": "9th4", "ט5": "9th5", "ט6": "9th6"
            }
            
            print("[+] getting user's class name|role|access code")
            class_raw = parts[6].strip()
            class_name = class_map.get(class_raw, class_raw)
            role = parts[7]
            access_code = parts[8]
            print("[+] getting current time")
            timeCreated = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[+] time created is: '{timeCreated}'")

            print("[+] opening data/users.json")
            with self.db_lock:
                try:
                    with open("data/users.json", "r", encoding='utf-8') as f:
                        print("[+] getting global users data")
                        global_users = json.load(f)
                        print("[+] suucessfuly got global users data")
                        
                except FileNotFoundError:
                    print("[*] did not find file data/users.json")
                    print("[*] assinging a an empty list")
                    global_users = {}
                    
                for u_name, data in global_users.items():
                    if data.get("gmail_account") == gmail:
                        print(f"[+] found email for user: {u_name}")
                        print(f"[+] sending gmail already exists to client: {addr}")
                        conn.sendall("gmail already exists".encode('utf-8'))
                        print(f"[+] successfuly sent gmail already exists to client: {addr}")
                        return

                if newUsername in global_users:
                    print("[+] found that username is in use")
                    print(f"[+] sending username already exists to client: {addr}")
                    conn.sendall("username already exists".encode('utf-8'))
                    print(f"[+] successfuly sent username already exists to client: {addr}")
                    return
            
            try:
                print("[+] oppening keys/teachers.key. hint: (teachers code file)")
                with open("keys/teachers.key", "r", encoding='utf-8') as f:
                    print("[+] successfuly oppened keys/teachers.key. hint: (teachers code file)")
                    print("[*] getting teachers code")
                    teacher_code = f.read().strip()
                    print("[+] got teachers code")
                    
                print("[+] oppening keys/students.key. hint: (students code file)")
                with open("keys/students.key", "r", encoding='utf-8') as f:  
                    print("[+] successfuly oppened keys/students.key. hint: (students code file)")
                    print("[*] getting students code")
                    student_code = f.read().strip()
                    print("[+] got students code")
                    
            except FileNotFoundError:
                print("[-] Key files missing!")
                print("[*] sending ")
                conn.sendall("error|server configuration error".encode("utf-8"))
                print("[*] successfult sent client side a server config error")
                return

            if role == "teacher" and access_code != teacher_code:
                conn.sendall("invalid teacher code".encode("utf-8"))
                return
            elif role == "student" and access_code != student_code:
                conn.sendall("invalid student code".encode("utf-8"))
                return
            elif role not in ["teacher", "student"]:
                conn.sendall("invalid role".encode("utf-8"))
                return
            
            class_file_path = f"classesStudents/{class_name}/students-{class_name}.json"
            with self.db_lock:
                try:
                    with open(class_file_path, "r", encoding='utf-8') as f:
                        class_users = json.load(f)
                        target_class = class_name

                        teacher_exists = any(user['role'] == 'teacher' and user['class'] == target_class 
                                            for user in class_users.values())

                        if teacher_exists and role == "teacher":
                            conn.sendall("teacher allready exists in this class".encode('utf-8'))
                            return
                            
                        if isinstance(class_users, list):
                            class_users = {u.get("username", str(i)): u for i, u in enumerate(class_users)}
                            
                except (FileNotFoundError, json.JSONDecodeError):
                    class_users = {}

                class_users[newUsername] = {
                    "id": len(class_users) + 1,
                    "first_name": firstName,
                    "last_name": lastName,
                    "gmail_account": gmail,
                    "role": role,
                    "class": class_name,
                    "tasks": [],
                    "created_at": timeCreated,
                    "grades": [] if role == "student" else "is teacher"
                    }
                
                os.makedirs(os.path.dirname(class_file_path), exist_ok=True)
                with open(class_file_path, "w", encoding='utf-8') as f:
                    json.dump(class_users, f, indent=4, ensure_ascii=False)
                    print(f"[+] successfully updated class file for {class_name}")

                salt, hashed_tuple = hashingAlg.hash_new_password(newPassword)
                password_to_save = f"{salt.hex()}:{hashed_tuple.hex()}"
                
                global_users[newUsername] = {
                    "id": len(global_users) + 1,
                    "password": password_to_save,
                    "first_name": firstName,
                    "last_name": lastName,
                    "gmail_account": gmail,
                    "role": role,
                    "class": class_name,
                    "created_at": timeCreated
                }
                
                with open("data/users.json", "w", encoding='utf-8') as f:
                    json.dump(global_users, f, indent=4, ensure_ascii=False)
                    print("[+] successfully updated global users.json")
            
            conn.sendall(f"200 ok|{role}|{class_name}".encode('utf-8'))

        def handle_get_schedule(self, conn, dataFromClient):
            class_name = dataFromClient.split("|")[1]
            try:
                with self.db_lock:
                    with open("data/schedule.json", "r", encoding="utf-8") as f:
                        schedules = json.load(f)
                        class_schedule = schedules.get(class_name, {})
                        conn.sendall(json.dumps(class_schedule, ensure_ascii=False).encode('utf-8'))
            except FileNotFoundError:
                conn.sendall("error|file not found".encode('utf-8'))

        def handle_get_tasks(self, conn, dataFromClient):
            parts = dataFromClient.split("|")
            class_name, username = parts[1], parts[2]
            
            with self.db_lock:
                try:
                    with open(f"classesStudents/{class_name}/students-{class_name}.json", "r", encoding='utf-8') as f:
                        students = json.load(f)
                        
                        if username in students:
                            print(f"[+] found that '{username}' is in students, proceeding...")
                            raw_tasks = students[username].get("tasks", [])
                            
                            if raw_tasks == "no tasks": tasks_list = [] 
                            elif isinstance(raw_tasks, str): tasks_list = [raw_tasks]  
                            else: tasks_list = raw_tasks
                                
                            response = json.dumps(tasks_list, ensure_ascii=False)
                            conn.sendall(response.encode('utf-8'))
                        else:
                            conn.sendall(f"username: '{username}' is not in this class?!".encode('utf-8'))
                except FileNotFoundError:
                    conn.sendall("error|class file not found".encode('utf-8'))

        def handle_update_tasks(self, conn, dataFromClient):
            parts = dataFromClient.split("|", 3) 
            if len(parts) < 4:
                conn.sendall("400 bad request".encode('utf-8'))
                return

            class_name, username, new_tasks_json = parts[1], parts[2], parts[3]
            file_path = f"classesStudents/{class_name}/students-{class_name}.json"
            
            with self.db_lock:
                try:
                    with open(file_path, "r", encoding='utf-8') as f:
                        all_students = json.load(f)

                    if username in all_students:
                        all_students[username]["tasks"] = json.loads(new_tasks_json)
                        with open(file_path, "w", encoding='utf-8') as f:
                            json.dump(all_students, f, indent=4, ensure_ascii=False)
                        
                        conn.sendall("200 ok".encode('utf-8'))
                        print(f"[+] Tasks updated for {username} in {class_name}")
                    else:
                        conn.sendall("user not found".encode('utf-8'))
                except Exception as e:
                    print(f"[-] Error updating tasks: {e}")
                    conn.sendall(f"error|{e}".encode('utf-8'))

        def handle_client(self, conn, addr):
            with conn:
                print(f"[+] New connection from {addr}")
                try:
                    rawDataFromClient = conn.recv(1024)
                    print("[+] handling client")
                    print("[+] listening")
                    if not rawDataFromClient:
                        return
                    
                    dataFromClient = rawDataFromClient.decode('utf-8').strip()
                    
                    if dataFromClient.startswith("login|"):
                        print("[+] received sensitive data. cannot show info") 
                        self.handle_login(conn, addr, dataFromClient)
                        
                    elif dataFromClient.startswith("signUp|"):
                        print("[+] received sensitive data. cannot show info") 
                        self.handle_signup(conn, addr, dataFromClient)
                        
                    elif dataFromClient == "freer premition":
                        print(f"[+] sending '200 ok' to client: {addr}")
                        conn.sendall("200 ok".encode('utf-8'))
                        print("[+] sent.")
                        
                    elif dataFromClient.startswith("get_schedule|"):
                        print(f"[+] subject received: get_schedule | ({addr})")
                        self.handle_get_schedule(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("tasks|"):
                        print(f"[+] subject received: tasks | ({addr})")
                        self.handle_get_tasks(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("update_tasks|"):
                        print(f"[+] subject received: update_tasks | ({addr})")
                        self.handle_update_tasks(conn, dataFromClient)
                        
                    elif dataFromClient == "guest":
                        with self.db_lock:
                            with open("data/server_connection_logs.json", "a", encoding="utf-8") as f:
                                log_fields = {
                                    "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                    "address": str(addr),
                                    "status": "guest"
                                }
                                print(f"[+] writing a connection log for guest: {addr}")
                                f.write(json.dumps(log_fields, ensure_ascii=False) + "\n")
                                print("[+] completed writing the connection log.")
                                conn.sendall("200 ok".encode('utf-8'))
                                return
                        
                    else:
                        print(f"[+] Unknown command received: {dataFromClient} | ({addr})")
                        
                except ValueError as e:
                    print(f"[+] Error handling client {addr}: {e}")
                except Exception as e:
                    print(f"[+] General error with client {addr}: {e}")

        def start(self):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            print("opening server key and crt")
            context.load_cert_chain("keys/server.crt", "keys/server.key")
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"[+] Server is listening on port: '{self.port}'")
                
                with context.wrap_socket(s, server_side=True) as ss:
                    while True:
                        try:
                            conn, addr = ss.accept()
                            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                            client_thread.start()
                        except Exception as e:
                            print(f"[-] Error accepting connection: {e}")

    if __name__ == "__main__":
        server = Server()
        server.start()

except KeyboardInterrupt:
    print("\n[+] KeyboardInterrupt! QUITTING...")