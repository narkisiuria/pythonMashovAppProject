# main.py

import tkinter as tk
from tkinter import messagebox
import login as l 
import time
from tkinter import ttk

# משתנים גלובליים למעקב אחר החלון הנוכחי והמשתמש המחובר

current_toplevel_win = None
current_username = ""
splash_root = None

def destroy_and_set_new_window(new_win):
    """הורס את החלון הנוכחי ושומר את הפניה לחלון החדש."""
    global current_toplevel_win
    if current_toplevel_win is not None and current_toplevel_win.winfo_exists():
        current_toplevel_win.destroy()
    current_toplevel_win = new_win

###########################################################
#               מסך פתיחה חדש                 #
###########################################################

def open_splash_screen():
    """יוצר מסך פתיחה מודרני מעוצב."""
    global splash_root
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    splash_root.geometry("420x580")

    # 🎨 צבעים מודרניים
    TEXT_MAIN = "white"
    TEXT_SUB = "#e0e0e0"
    BTN_BG = "#ffffff"
    BTN_FG = "#4a00e0"

    # יצירת רקע גרדיאנט
    canvas = tk.Canvas(splash_root,
                       width=420,
                       height=580,
                       highlightthickness=0,
                       bd=0)
    
    canvas.pack(fill="both",
                expand=True)

    for i in range(580):
        r = int(74 + (142 - 74) * (i / 580))
        g = int(0 + (45 - 0) * (i / 580))
        b = int(224 + (226 - 224) * (i / 580))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, 420, i, fill=color)

    canvas.create_text(210,
                       110,
                       text="משוב",
                       fill=TEXT_MAIN,
                       font=("Arial",
                             46, "bold"))
    
    canvas.create_text(210,
                       170,
                       text="ניהול לימודים חכם • פשוט • מהיר",
                       fill=TEXT_SUB,
                       font=("Arial", 16))
    
    canvas.create_text(210,
                       285,
                       text="📊",
                       font=("Arial", 97))

    def create_button():
        btn = tk.Button(
            splash_root,
            text="התחבר עכשיו",
            font=("Arial", 18, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            bd=0,
            relief="flat",
            width=14,
            cursor="hand2",
            command=open_login_window
        )

        tk.Button(
            splash_root,
            text="הצצה מהירה",
            font=("Arial", 16, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            bd=0,
            relief="flat",
            width=10,
            cursor="hand2",
            command=open_peak).place(x=142, y=446)
        
        canvas.create_window(210, 400, window=btn)

    create_button()

    canvas.create_text(210, 540,
                       text="© 2025 Mashov - כל הזכויות שמורות",
                       fill="#eeeeee",
                       font=("Arial", 10))

    canvas.create_text(210, 510,
                    text="© מפתח האפליקציה - אוריה נרקיסי",
                    fill="#eeeeee",
                    font=("Arial", 10))
    
    # למרכז המסך
    splash_root.update_idletasks()
    w = splash_root.winfo_screenwidth()
    h = splash_root.winfo_screenheight()
    size = tuple(int(_) for _ in splash_root.geometry().split('+')[0].split('x'))
    x = (w/2) - (size[0]/2)
    y = (h/2) - (size[1]/2)
    splash_root.geometry(f"{size[0]}x{size[1]}+{int(x)}+{int(y)}")

    splash_root.mainloop()

###########################################################
#                   מסך לוגין                   #
###########################################################

def open_login_window():
    global splash_root
    if splash_root:
        splash_root.destroy()
    root.deiconify()  

###########################################################
#                      עמוד ראשי               #
###########################################################

def open_peak():
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    
    new_win.title("עמוד ראשי")
    new_win.geometry("400x620")

    tk.Label(new_win, 
             font="Arial 10 bold").pack(side="top", pady=(10,0))
    tk.Label(new_win, 
             text="?מה ברצונך לעשות", 
             font="Arial 16 bold").pack(side="top")

    tk.Button(new_win, 
              text="מערכת שעות", 
              fg="white", 
              bg="#8a1476", 
              font="Arial 14", 
              width=13, 
              height=6,
              bd=0,
              command=open_marechet,
              cursor="hand2",).place(x=25, y=90)

    tk.Button(new_win, 
              text="דואר נכנס", 
              fg="white", 
              bg="#ff5500", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_doar,
              cursor="hand2",).place(x=217, y=90)

    tk.Button(new_win, 
              text="ציונים שוטפים", 
              fg="white", 
              bg="#05a005", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_grades,
              cursor="hand2",).place(x=25, y=265)

    tk.Button(new_win, 
              text="נוכחות בשיעור", 
              fg="white", 
              bg="#2302b9", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_attendance,
              cursor="hand2",).place(x=217, y=265)

    tk.Button(new_win,
              text="תזכורון", 
              fg="white", 
              bg="#f000c8", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_reminder,
              cursor="hand2",).place(x=25, y=440)

    tk.Button(new_win, 
              text="שיחרורון", 
              fg="white", 
              bg="#0195af", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_freer,
              cursor="hand2",).place(x=217, y=440)

def open_main_page(username):
    global current_username
    
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    current_username = username
    
    new_win.title("עמוד ראשי")
    new_win.geometry("400x620")

    tk.Label(new_win, 
             text=f"{(username)}", 
             font="Arial 10 bold").pack(side="top", pady=(10,0))
    tk.Label(new_win, 
             text="?מה ברצונך לעשות", 
             font="Arial 16 bold").pack(side="top")

    tk.Button(new_win, 
              text="מערכת שעות", 
              fg="white", 
              bg="#8a1476", 
              font="Arial 14", 
              width=13, 
              height=6,
              bd=0,
              command=open_marechet,
              cursor="hand2",).place(x=25, y=90)

    tk.Button(new_win, 
              text="דואר נכנס", 
              fg="white", 
              bg="#ff5500", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_doar,
              cursor="hand2",).place(x=217, y=90)

    tk.Button(new_win, 
              text="ציונים שוטפים", 
              fg="white", 
              bg="#05a005", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_grades,
              cursor="hand2",).place(x=25, y=265)

    tk.Button(new_win, 
              text="נוכחות בשיעור", 
              fg="white", 
              bg="#2302b9", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_attendance,
              cursor="hand2",).place(x=217, y=265)

    tk.Button(new_win,
              text="תזכורון", 
              fg="white", 
              bg="#f000c8", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_reminder,
              cursor="hand2",).place(x=25, y=440)

    tk.Button(new_win, 
              text="שיחרורון", 
              fg="white", 
              bg="#0195af", 
              font="Arial 14", 
              width=13,
              height=6,
              bd=0,
              command=open_freer,
              cursor="hand2",).place(x=217, y=440)

###########################################################
#                   פונקציית התחברות           #
###########################################################

def attempt_login():
    username = entry_username.get()
    password = entry_password.get()
    try:
        password = int(password)
    except ValueError:
        time.sleep(1)
        messagebox.showerror("שגיאה", "סיסמה חייבת להיות מספר")
        return

    if username == "admin" or (username == "brientheking67" and password == 1235):
        time.sleep(1)
        open_main_page(username)
        root.withdraw()
    else:
        time.sleep(1)
        messagebox.showerror("שגיאה", "שם משתמש או סיסמה לא נכונים")



###########################################################
#                      עמוד פתיחה                  #
###########################################################

def forgotpass():
    messagebox.showinfo(title="?שכחת את הסיסמה", message="שנה את סיסמתך במשרד המזכירות בבית הספר")


def p_p():
    messagebox.showinfo(title="מדיניות והפרטיות", message="קיצר, אנחנו מחליטים על בערך הכל")



root = tk.Tk()
root.title("Mashov App/Login")
root.geometry("400x550")
root.configure(bg="lightgreen")
root.withdraw()


tk.Label(root, 
          text="ברוך הבא לאפליקצית המשוב\n כדי להתחיל\n בבקשה תכניס את שם המשתמש והסיסמה שלך ", 
          font="Arial 14 bold", 
          bg="lightgreen").pack(side="top", pady=(50,0))

tk.Label(root, text="שם משתמש", font="Arial 14", bg="lightgreen").pack(pady=(40, 10))
entry_username = tk.Entry(root, width=25, bg="white")
entry_username.pack()

tk.Label(root, text="סיסמה", font="Arial 14", bg="lightgreen").pack(pady=(10,0))
entry_password = tk.Entry(root, width=25, bg="white", show="*")
entry_password.pack(pady=7)

tk.Button(root,
           text="התחברות", 
           font=14, 
           command=attempt_login,
          bg="royalblue", 
          fg="white", 
          bd=0, 
          width=20,
          cursor="hand2",).pack(pady=20)

tk.Button(root, 
          text="?שכחת את הסיסמה", 
          font=5, 
          command=forgotpass,
          bg="lightgreen", 
          fg="blue", 
          bd=0,
          cursor="hand2",).pack()

tk.Label(root, 
         text="בכך שאתה מכניס את שם המשתמש והסיסמה שלך\n אתה בעצם מסכים עם כל ה\n", 
          font="Arial 11 bold", 
          bg="lightgreen").pack(pady=(40,0))

tk.Button(root, 
          text="המדיניות והפרטיות שלנו", 
          font=5, 
          command=p_p,
          bg="lightgreen", 
          fg="red", 
          bd=0,
          cursor="hand2",).pack()



###########################################################
#                שערי האפליקציה        #
###########################################################

def open_grades():
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    new_win.title("עמוד ציונים")
    new_win.geometry("400x620")

    tk.Button(new_win, 
              text="חזרה למסך ראשי",
              command=lambda: open_main_page(current_username),
              cursor="hand2",).place(x=10, y=10)

    tk.Label(new_win, 
             text="ציונים שוטפים", 
             font="Arial 21 bold").place(x=110, y=45)


def open_doar():
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    new_win.title("עמוד דואר")
    new_win.geometry("400x620")

    tk.Button(new_win, 
              text="חזרה למסך ראשי",
              command=lambda: open_main_page(current_username),
              cursor="hand2",).place(x=10, y=10)

    tk.Label(new_win, text="אין דואר", font="Arial 21 bold").place(x=150, y=45)


def open_attendance():
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    new_win.title("עמוד נוכחות")
    new_win.geometry("400x620")

    tk.Button(new_win, 
              text="חזרה למסך ראשי",
              command=lambda: open_main_page(current_username),
              cursor="hand2",).place(x=10, y=10)

    tk.Label(new_win, 
             text="נוכחות בשיעור", 
             font="Arial 21 bold",
             fg="blue").place(x=110, y=40)
    
    ttk.Combobox(new_win,
                 text="כיתה",
                 values=["ט'1", "ט'2", "ט'3", "ט'4", "ט'5", "ט'6"],
                 font="Arial 13",
                 width=5).place(x=260, y=110)

    tk.Label(new_win,
             text="נרקיסי אוריה",
             font="Arial 13",
             fg="blue",
             ).place(x=260, y=140)
    
    ttk.Combobox(new_win,
                 values=["נוכחות", "תרומה לשיעור", "היעדרות", "הפרעה", "אי הכנת שיעורי בית", "הכין שיעורי בית כמו גדול"]).place(x=180, y=200)
    

def open_reminder():
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    new_win.title("עמוד תזכורון")
    new_win.geometry("400x620")

    def reminder_completed():
        time.sleep(1)
        if classt.get() == "" or keep_an_eye.get() == "" or remind.get() == "" or techer.get() == "" or did_today.get() == "" or didnt_do.get() == "" or preper.get() == "" or start_leason.get() == "" or focus.get() == "":
            messagebox.showerror("שגיאה", "בבקשה תמלא את כל הפרטים שבתופס")
        else:
            messagebox.showinfo("בקשת שחרור מוצלחת", "!בקשת השחרור אושרה בהצלחה")


    tk.Button(new_win, 
              text="חזרה למסך ראשי",
              command=lambda: open_main_page(current_username),
              cursor="hand2",).place(x=10, y=10)

    tk.Label(new_win, text="תזכורון", font="Arial 21 bold",
             fg="blue").place(x=155, y=45)
    
    tk.Label(new_win,
             text="פה תכתוב פתקים לשיעור הבא שלך",
             fg="blue",
             font="Arial 14").place(x=75, y=90)
    
    tk.Label(new_win,
             text="כיתה",
             font="Arial 14 bold",
             fg="blue").place(x=315,y=145)
    
    classt = ttk.Combobox(new_win,
                 width=4,
                 values=["ט'1", "ט'2", "ט'3", "ט'4", "ט'5", "ט'6"],
                 state="readonly",
                 font="Arial 12")
    classt.place(x=250, y=145)

    tk.Label(new_win,
             text="מורה",
             font="Arial 14 bold",
             fg="blue").place(x=185,y=145)
    
    techer = ttk.Combobox(new_win,
                 width=9,
                 values=["הרב שלומי", "אוריה דביר", "יעל אלבז", "המנהל נועם", "נועם שיף", "הרב יעקב"],
                 state="readonly",
                 font="Arial 12" )
    techer.place(x=75, y=145)   
    

    tk.Label(new_win,
             text="?מה עשינו היום",
             font="Arial 12 bold",
             fg="blue",).place(x=288, y=210)

    did_today = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    did_today.place(x=114, y=210)         

    tk.Label(new_win,
             text="?מה צריך להספיק",
             font="Arial 12 bold",
             fg="blue",).place(x=274, y=250)

    didnt_do = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    didnt_do.place(x=100, y=250) 

    tk.Label(new_win,
             text="?מה צריך להכין לשיעור הבא",
             font="Arial 12 bold",
             fg="blue",).place(x=209, y=290)

    preper = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    preper.place(x=35, y=290) 
    
    tk.Label(new_win,
             text="?איך אני אתחיל את השיעור",
             font="Arial 12 bold",
             fg="blue",).place(x=215, y=330)

    start_leason = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    start_leason.place(x=43, y=330) 

    tk.Label(new_win,
             text="?על מה להתפקס בשיעור",
             font="Arial 12 bold",
             fg="blue",).place(x=228, y=370)

    focus = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    focus.place(x=56, y=370) 
    
    tk.Label(new_win,
             text="תזכורת לשיעור הבא",
             font="Arial 12 bold",
             fg="blue",).place(x=259, y=410)

    remind = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    remind.place(x=89, y=410) 

    tk.Label(new_win,
             text="?על מי צריך לשים עין",
             font="Arial 12 bold",
             fg="blue",).place(x=253, y=450)

    keep_an_eye = ttk.Entry(new_win,
              font="Arial 11",
              width=20,)
    keep_an_eye.place(x=82, y=450)

    tk.Label(new_win, 
             text="בלחיצה על כפתור שמירת הטופס אני מאפשר\n גישה מלאה לקבצים שלי",
             font="Arial 11 bold", 
             fg="blue").place(x=60, y=500) 
    
    tk.Button(new_win,
              text="אישור הטופס",
              font="Arial 10 bold",
              bg="blue",
              fg="ghostwhite",
              bd=0,
              width=11,
              height=2,
              activebackground="lightblue",
              command=reminder_completed,
              cursor="hand2",).place(x=13, y=560)

def open_freer():
    global days, id_s, id, hr, rs

    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)
    new_win.title("עמוד שיחרורון")
    new_win.geometry("400x620")

    tk.Button(new_win, 
              text="חזרה למסך ראשי",
              command=lambda: open_main_page(current_username),
              cursor="hand2",).place(x=10, y=10)

    tk.Label(new_win,
             text="טופס בקשת שחרור",
             font="Arial 20 bold",
             fg="blue",
             cursor="hand2",).place(x=125, y=30)

    tk.Label(new_win, text="ת.ז. של התלמיד/ה", fg="blue", font="Arial 12 bold").place(x=245, y=93)

    id_s = tk.Entry(new_win, width=32, font="Arial 15")
    id_s.place(x=17, y=130)

    tk.Label(new_win, text="ת.ז. שלך (ההורה)", fg="blue",
             font="Arial 12 bold").place(x=250, y=175)

    id = tk.Entry(new_win, width=32, font="Arial 15")
    id.place(x=17, y=210)

    tk.Label(new_win,
             text="יום השחרור",
             fg="blue",
             font="Arial 12 bold").place(x=294, y=252)

    days = ttk.Combobox(new_win, width=32, font="Arial 15",
                         values=["יום ראשון", "יום שני", "יום שלישי", "יום רביעי", "יום חמישי"],
                         state="readonly")
    days.place(x=17, y=285)

    tk.Label(new_win, text="שעה", fg="blue", font="Arial 12 bold").place(x=335, y=325)

    hr = ttk.Combobox(new_win, width=32, font="Arial 15",
                      values=["9:00", "9:30", "10:00", "10:30",
                              "11:00", "11:30", "12:00", "12:30",
                              "13:00", "13:30", "14:00", "14:30",
                              "15:00", "15:30", "16:00"],
                      state="readonly")
    hr.place(x=17, y=355)

    tk.Label(new_win,
             text="סיבה \\ הערה",
             fg="blue",
             font="Arial 12 bold").place(x=286, y=400)

    rs = tk.Entry(new_win, width=32, font="Arial 15")
    rs.place(x=17, y=430)

    tk.Label(new_win, 
             text="בלחיצה על הכפתור בקשת שחרור אני מסכימ\\ה לתנאי \n"
                  "השימוש והמדיניות/פרטיות המאפשרת לקבלת מיילים/סמסים",
             font="Arial 11 bold", 
             fg="blue").place(x=15, y=495)

    tk.Button(new_win,
              text="בקשת שחרור",
              font="Arial 10 bold",
              bg="blue",
              fg="ghostwhite",
              bd=0,
              width=11,
              height=2,
              activebackground="lightblue",
              command=freer_completed,
              cursor="hand2",).place(x=13, y=560)

def freer_completed():
    time.sleep(1)
    if days.get() == "" or id.get() == "" or id_s.get() == "" or hr.get() == "" or rs.get() == "":
        messagebox.showerror("שגיאה", "בבקשה תמלא את כל הפרטים שבתופס")
    else:
        messagebox.showinfo("בקשת שחרור מוצלחת", "!בקשת השחרור אושרה בהצלחה")

def open_marechet():
    new_win = tk.Toplevel()
    destroy_and_set_new_window(new_win)

    new_win.title("עמוד מערכת")
    new_win.geometry("400x620")

    tk.Button(new_win, 
              text="חזרה למסך ראשי",
              command=lambda: open_main_page(current_username),
              cursor="hand2",).place(x=10, y=10)

    tk.Label(new_win, text="מערכת", font="Arial 21 bold").place(x=155, y=45)
    

if __name__ == "__main__":
    open_splash_screen()
