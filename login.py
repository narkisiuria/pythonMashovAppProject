# login.py

def login():
    print("Welcome! Please login:")
    while True:
        username = input("Username: ")
        try:
            password = int(input("Password: "))
        except ValueError:
            print("Password must be a number.")
            continue

        if username == "admin":
            return username
        elif username == "brientheking67" and password == 1235:
            return username
        else:
            print("Incorrect username or password. Try again.")
