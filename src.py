# src.py

try:
    import time
    grades = {
        "uria": 100,
        "ranen": 90,
        "ido": 85
    }
    notes = {
        "what have we done today?": "1",
        "what havent we done today?": "2",
        "what do i need to preper for my next leason?": "3",
        "how shuld i start my next leason?": "4",
        "on what shuld i focus?": "5",
        "exresises for the end of the leason & homework:": "6",
        "a reminder for my next leason:": "7"
    }
    def print_dict(grades):
        for key, value in grades.items():
            print(f"{key}: {value}")
    def highest_grade(grades):
        return max(grades.values())
    def lowest_grade(grades):
        return min(grades.values())
    def average_grade(grades):
        return round(sum(grades.values()) / len(grades.values()), 2)
    password = ""
    username = ""
    command = ""
    why_ido = ""
    why_ranen = ""
    why_uria = ""
    reason2 = ""
    reason = ""
    reason1 = ""
    print("")
    print("uploading files...")
    time.sleep(2)
    print("prepering app...")
    time.sleep(2)
    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("hello, welcome to the mashov app!")
    while True:
        print("to get started please enter your username & password:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        username = input("username: ")
        password = int(input("password: "))
        print("")
        print("Laoding...")
        time.sleep(1.5)
        if username == "admin":
            break
        elif password  == 1235 and username == "brientheking67":
            break
        else:
            print("")
            print("username or password are incorrect! ")
            print("")
    print("")
    time.sleep(1.5)
    print("welcome back!", username)
    print("")
    print('''what are your plans for today:
1. Attendance
2. grading system
3. plan your next leason''')
    print("")
    plan = input("> ")
    if plan == "1":
        print("")
        print("uploading...")
        print("")
        time.sleep(2)
        grade_class = input("from what class: ")
        if grade_class == "9th grade":
            print("")
            print("loading class...")
            time.sleep(1.7)
            print('''
1. To mark as atended
2. To mark as didnt attend
3. To mark as disarapted
4. To give a bonus''')
            print("")
            uria_atnd = input("uria: ")
            if uria_atnd == "2":
                uria_atnd = "didnt attend"
            elif uria_atnd == "3":
                why_uria = input("reason: ")  
                reason = "reason"  
                uria_atnd = "disarapted"
            elif uria_atnd == "1":
                uria_atnd = "attended"
            elif uria_atnd == "4":
                uria_atnd = "attended + bonus"    
        
            ranen_atnd = input("ranen: ")
            if ranen_atnd == "2":
                ranen_atnd = "didnt attend"
            elif ranen_atnd == "3":
                why_ranen = input("reason: ")
                reason1 = "reason"
                ranen_atnd = "disarapted"   
            elif ranen_atnd == "1":
                ranen_atnd = "attended"
            elif ranen_atnd == "4":
                ranen_atnd = "attended + bonus"    
        
            ido_atnd = input("ido: ")
            if ido_atnd == "2":
                ido_atnd = "didnt attend"
            elif ido_atnd == "3":
                why_ido = input("reason: ")  
                reason2 = "reason"
                ido_atnd = "disarapted"  
            elif ido_atnd == "1":
                ido_atnd = "attended"
            elif ido_atnd == "4":
                ido_atnd = "attended + bonus"        
            else:
                print("please choose (1, 2 or 3)")    
            print("")
            print("sumerising...")
            time.sleep(2)
            print("")
            print(f'''result:
uria: {uria_atnd}, {reason} {why_uria}
ranen: {ranen_atnd}, {reason1} {why_ranen}
ido: {ido_atnd}, {reason2} {why_ido}''')
            print("")
            while True:
                send = input("send mashov? (y/n)> ").lower
                if send == "n":
                    print("the mashov did not go throught")
                    break
                else:
                    print("")
                    print("sending mashov...")
                    time.sleep(2)
                    print("")
                    print("mashov sent sucssesfuly")  
                    print("")
                    print("closing app...")
                    time.sleep(1.9)  
                    print("")
                    print("thank you for choosing masohv!")
                    break
    while True:
        if plan == "2":  
            print("")
            print("uploading...")
            time.sleep(2)
            if True:
                print("")
                print('''1. To see all grades
2. To see a specific grade
3. To change a student's grade
4. To see the highest grade
5. To see the lowest grade
6. To see the average grade''')
                remove = ""
                add = ""
                print("")
                plan2 = input("> ")
                if plan2 == "1":
                    print("")
                    print("loading files...")
                    time.sleep(1.2)
                    print("")
                    print("grades:")
                    print("")
                    print_dict(grades)
                elif plan2 == "2":
                    print("")
                    name = input("child's name: ")
                    print("")
                    result = grades.get(name, "no such a name")
                    print(f"{name}'s grade: {result}")
                elif plan2 == "3":
                    print("")
                    change_kids_grade = input("change whose grade? ")
                    change = int(input(f"change {change_kids_grade}'s grade to: ")) 
                    if change_kids_grade == "uria":
                        grades["uria"] = change
                    elif change_kids_grade == "ranen":
                        grades["ranen"] = change
                    elif change_kids_grade == "ido":
                        grades["ido"] = change    
                    print("")
                    print("changing grade...")
                    time.sleep(1.7)
                    print("")
                    print("grade changed sucssesfuly!") 
                elif plan2 == "4":
                    print("")
                    print("calculating...")
                    time.sleep(1.6)
                    print("")
                    print("highest grade is:", highest_grade(grades))
                elif plan2 == "5":
                    print("")
                    print("calculating...")
                    time.sleep(1.6)
                    print("")
                    print("lowest grade is:", lowest_grade(grades))
                elif plan2 == "6":
                    print("")
                    print("calculating...")
                    time.sleep(1.6)
                    print("")
                    print("average:", average_grade(grades))
        if plan == "3":
            print("")
            print("uplaoding...")
            time.sleep(1.6)
            print("")
            print('''1. to take new notes for my next class
2. To see my last taken notes''')
            print("") 
            todoplan = input("> ")
            if todoplan == "2":
                print("")
                print("uplaoding your notes...")
                time.sleep(1.7)
                print("")
                print("what have we done today:","".join(notes["what have we done today?"]))
                print("")
                print("what havent we done today:","".join(notes["what havent we done today?"]))
                print("")
                print("what do i need to preper for my next leason?","".join(notes["what do i need to preper for my next leason?"]))
                print("")
                print("how shuld i start my next leason:","".join(notes["how shuld i start my next leason?"]))
                print("")
                print("on what shuld i focus:","".join(notes["on what shuld i focus?"]))
                print("")
                print("exresises for the end of the leason & homework:","".join(notes["exresises for the end of the leason & homework:"]))
                print("")
                print("a reminder for my next leason:","".join(notes["a reminder for my next leason:"]))
                print("")
            if todoplan == "1":        
                print("")
                print("start taking your notes for your next leason in here:")  
                print("")
                time.sleep(1)  
                suply = input("what have we done today?: ")    
                suply = notes["what have we done today?"] = [suply]
                print("")
                suply2 = input("what havent we done today?: ")
                suply2 = notes["what havent we done today?"] = [suply2]
                print("")
                suply3 = input("what do i need to preper for my next leason?: ")
                suply3 = notes["what do i need to preper for my next leason?"] = [suply3]
                print("")
                suply4 = input("how shuld i start my next leason?: ") 
                suply4 = notes["how shuld i start my next leason?"] = [suply4]
                print("")
                suply5 = input("on what shuld i focus?: ")
                suply5 = notes["on what shuld i focus?"] = [suply5]
                print("")
                suply6 = input("exresises for the end of the leason & homework: ")
                suply6 = notes["exresises for the end of the leason & homework:"] = [suply6]
                print("")
                suply7 = input("a reminder for my next leason: ")
                suply7 = notes["a reminder for my next leason:"] = [suply7]
                print("")
                print("adding to your last taken notes...")
                time.sleep(2)
                print("")
                print("done sucssesfuly")

except ValueError:
    print("please enter a number.")
except TypeError:
    print("i dont know... what have you done?")    
except Exception:
    print("idk error, check what you have typed and try again.")