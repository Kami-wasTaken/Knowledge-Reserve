from tkinter import *
from tkinter import ttk
import mysql.connector
import smtplib
from email.message import EmailMessage


root = Tk()

#======================================================initiate
root.geometry("1280x720")
root.title("Knowledge reserve")
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

#============================================================Connect to database
db = mysql.connector.connect(
    host="brbjmpkm2lgsjfy1lfhx-mysql.services.clever-cloud.com",
    user="ukc8u9srhpdpi6qv",
    passwd="VPG7dB5QxCWQvMyUaWIw",
    database="brbjmpkm2lgsjfy1lfhx"
)
mycursor = db.cursor()

#========================================================Email
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "knowledgereserveexchange@gmail.com"
    msg['from'] = user
    password = "azefgkotntxrtppr"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    print(to)
      



#===================================================Functions

def toggle_password(entry):
    if entry.cget('show') == '':
        entry.config(show='*')
    else:
        entry.config(show='')
        


    


def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()
   print("function called")

def updateaccount():
    book1 = dp1.get()
    book2 = dp2.get()
    book3 = dp3.get()
    username = Email_entry.get()
    mycursor.execute("UPDATE booksavailable SET bookslot1 = %s, bookslot2 = %s, bookslot3 = %s WHERE username = %s", (book1, book2, book3, username))
    
    db.commit()

def viewbooks(book1, book2, book3):
    username = Email_entry.get()
    mycursor.execute("SELECT * FROM booksavailable WHERE username = %s", (username,))
    books = mycursor.fetchall()

    for row in books:
        book1.set(str(row[1]))
        book2.set(str(row[2]))
        book3.set(str(row[3]))
    print(books)

def showresults():
    y = Search_Bar.get()
    count = 0
    clear_frame(results_bg1)
    clear_frame(results_bg2)
    mycursor.execute("Select username FROM booksavailable WHERE bookslot1 = %s OR bookslot2 = %s OR bookslot3 = %s", (y,y,y))
    results = mycursor.fetchall()
    a = []
    i = 0
    e = 0
    j = 0
    for i in range (len(results)):
        print("e = " + str(e))
        b = []
        a.extend(list(results[i]))
        a_ = a[i]
        mycursor.execute("SELECT email FROM accounts WHERE username = %s", (a_,))
        value = mycursor.fetchone()
        if e <= 300:
            book_result(y, a[i], 0, e, y, value, results_bg1)
            e += 300 
        else:
            book_result(y, a[i], 0, j, y, value, results_bg2)
            j += 300 
        
        print(a[i])
        count += 1
    previousbutton = Button(frame5, text="previous",font=("Roboto", 15, "bold"), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:show_frame(results_bg1))
    nextbutton = Button(frame5, text="next",font=("Roboto", 15, "bold"), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:show_frame(results_bg2))
    if  count > 2:
        nextbutton.place(x = 130, y = 350,  width = 100, height = 40)
        previousbutton.place(x = 30, y = 350,  width = 100, height = 40)
    else:
        previousbutton.destroy()
        nextbutton.destroy()

    print(count)
    print(a)


        



def login(frame):
    username = Email_entry.get()
    password = Password_entry.get()
    mycursor.execute("Select password, username FROM accounts WHERE username = %s", (username,))
    result = mycursor.fetchall()
    if (password,username) in result:
        frame.tkraise()
    else:
        invalid = Label(frame1, text="The credentials are invalid", font=("Roboto", 16), fg = "Red", bg ="#FE9959")
        invalid.place(x = 510, y = 620)


def sign_up(frame):
    email = (Email_entryS.get())
    username1 = UN_textS.get()
    password2 = Password_entryS.get()
    none = 'none'
    entry = (email, password2, username1)
    mycursor.execute("SELECT username FROM accounts")
    SQLformula = "INSERT INTO accounts (email, password, username) VALUES (%s, %s, %s)"
    result = mycursor.fetchall()
    if (username1,) in result:
        print("This username already exists")
        alrexists = Label(frame2, text="This username already exists", font=("Roboto", 16), fg = "Red", bg ="#FE9959")
        alrexists.place(x = 490, y = 650)
    else: 
        mycursor.execute(SQLformula,entry)
        mycursor.execute("INSERT INTO booksavailable (username, bookslot1, bookslot2, bookslot3) VALUES (%s, %s, %s, %s)", (username1, none, none, none))
        frame.tkraise()
        db.commit()
    

def show_frame(frame):
    frame.tkraise()

def reset_text(frame,e, text):
    frame.tkraise()
    e.delete(0,END)
    e.insert(0,text)
    return


def book_result(bookname, author, _x, _y, message, toperson, frame):
    username = Email_entry.get()
    bookframe = Frame(frame, bg="#E6E6EA", width="470", height="240")
    bookframe.place(x = 130 + _x, y = 100 + _y, width=470, height=240)
    ba = Label(bookframe, text="Availability: yes", font=("roboto", 18, "bold"), bg="#E6E6EA")
    sn = Label(bookframe, text="Seller name: " + author, font=("roboto", 18, "bold"), bg="#E6E6EA")
    bn = Label(bookframe, text = "Book name: " + bookname, font=("roboto", 18, "bold"), bg="#E6E6EA")
    mycursor.execute("SELECT email FROM accounts WHERE username = %s", (username,))
    result = mycursor.fetchall()
    for row in result:
        email = (str(row[0]))
    contact_button = Button(bookframe, text="Contact", font=("Roboto", 15, "bold"), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:email_alert("I am in need for "+message, "my email is "+ email +" please contact me", toperson))
    ba.place(x=140, y = 60)
    bn.place(x=55, y = 10)
    sn.place(x=65, y = 110)
    contact_button.place(x=150, y=170, width=160, height=50)
    return bookframe

#=========================================Frames
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)
frame5 = Frame(root)


#display
for frame in (frame1, frame2, frame3, frame4, frame5):
    frame.grid(row = 0 , column = 0, sticky = "nsew")

#=======================================================Login page code

lgbg = PhotoImage(file = "Login_BG.png")
sign_in_pagepic = PhotoImage(file = "Sign_pg.png")
eye_img = PhotoImage(file = "Eye_img.png")
Login_bg = Label(frame1, image = lgbg)
Login_bg.place(x = -2,y = -2)


Email_text = StringVar()
Email_text.set("Username")
Email_entry = Entry(frame1, textvariable = Email_text, font=("Roboto", 16), fg = "white", bg = "#F4A08E", justify='center', borderwidth=0)
Email_entry.place(x = 450, y = 350, width = 390, height = 50)

Password_text = StringVar()
Password_text.set("Password")
Password_entry = Entry(frame1,textvariable = Password_text, font=("Roboto", 16), fg = "white", bg = "#F4A08E", justify='center', borderwidth=0)
Password_entry.place(x = 450, y = 420, width = 390, height = 50)

eye1 = Button(frame1, image = eye_img,  borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:toggle_password(Password_entry))
eye1.place(x = 845, y = 430)

Login_bt = Button(frame1, text="Login", font=("Roboto", 15, "bold"), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:[login(frame3)])
Login_bt.place(x = 560, y = 500, width=160, height=50)

Signin_pagebt = Button(frame1, image=sign_in_pagepic, borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:[reset_text(frame2,Email_entry, "Username"), reset_text(frame2,Password_entry, "Password")])
Signin_pagebt.place(x = 710, y = 580)


#=======================================================Sign_up page code
spbg = PhotoImage(file = "Sign_BG.png")
login_in_pagepic = PhotoImage(file = "Login_pg.png")
SignUp_bg = Label(frame2, image = spbg)
SignUp_bg.place(x = -2,y = -2)

Email_textS = StringVar()
Email_textS.set("Email")
Email_entryS = Entry(frame2, textvariable = Email_textS, font=("Roboto", 16), fg = "white", bg = "#F4A08E", justify='center', borderwidth=0)
Email_entryS.place(x = 450, y = 396, width = 390, height = 50)

Password_textS = StringVar()
Password_textS.set("Password")
Password_entryS = Entry(frame2,textvariable = Password_textS, font=("Roboto", 16), fg = "white", bg = "#F4A08E", justify='center', borderwidth=0)
Password_entryS.place(x = 450, y = 475, width = 390, height = 50)

eye2 = Button(frame2, image = eye_img,  borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:toggle_password(Password_entryS))
eye2.place(x = 845, y = 485)

UN_textS = StringVar()
UN_textS.set("Username")
Un_entryS = Entry(frame2,textvariable = UN_textS, font=("Roboto", 16), fg = "white", bg = "#F4A08E", justify='center', borderwidth=0)
Un_entryS.place(x = 450, y = 322, width = 390, height = 50)

SignIn_bt = Button(frame2, text="Create", font=("Roboto", 15, "bold"), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:sign_up(frame1))
SignIn_bt.place(x = 560, y = 550, width=160, height=50)

Login_pagebt = Button(frame2, image=login_in_pagepic, borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:[reset_text(frame1,Email_entryS, "Email"), reset_text(frame1,Password_entryS, "Password"), reset_text(frame1,Un_entryS, "Username")])
Login_pagebt.place(x = 715, y = 624)

#=======================================================Selection page code
slbg = PhotoImage(file = "Selection_BG.png")
Lg_Bk = PhotoImage(file = "Bk_Login.png")
selection_bg = Label(frame3, image = slbg)
selection_bg.place(x = -2,y = -2)

Select1_bt = Button(frame3, text="Select", font=("Roboto", 15), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:show_frame(frame5))
Select1_bt.place(x = 830, y = 425, width=160, height=50)

Select2_bt = Button(frame3, text="Select", font=("Roboto", 15), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:[show_frame(frame4), viewbooks(n, m, o)])
Select2_bt.place(x = 280, y = 425, width=160, height=50)

n = StringVar()
m = StringVar()
o = StringVar()

Login_Backbt = Button(frame3, image=Lg_Bk, borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:[reset_text(frame1,Email_entry, "Username"), reset_text(frame1, Password_entry, "Password")])
Login_Backbt.place(x = 10, y = 690)

#=======================================================Book exchange page code
bebg = PhotoImage(file = "Exchange_BG.png")
bts = PhotoImage(file = "BTS_Btt.png")
exchange_bg = Label(frame4, image = bebg)
exchange_bg.place(x = -2,y = -2)

style = ttk.Style()
style.theme_use('classic')
style.configure("TCombobox", fieldbackground = "#2AB7CA", background = "#2AB7CA", arrowcolor="#2AB7CA")
  



dp1 = ttk.Combobox(frame4, width = 17, textvariable=n, font=("Roboto", 15), foreground="white")
dp2 = ttk.Combobox(frame4, width = 17, textvariable = m, font=("Roboto", 15), foreground="white")
dp3 = ttk.Combobox(frame4, width = 17, textvariable = o, font=("Roboto", 15), foreground="white")

dp1['values'] = ('Life Science (Holt Science And Technology)', 'Macbeth', 'Haese maths book 7', 'Haese maths book 9', 'Haese maths book 8', 'none')
dp2['values'] = ('Life Science (Holt Science And Technology)', 'Macbeth', 'Haese maths book 7', 'Haese maths book 9', 'Haese maths book 8', 'none')
dp3['values'] = ('Life Science (Holt Science And Technology)', 'Macbeth', 'Haese maths book 7', 'Haese maths book 9', 'Haese maths book 8', 'none')

dp1.place(x = 132, y = 360, width=200, height=50)
dp2.place(x = 537, y = 360, width=200, height=50)
dp3.place(x = 952, y = 360, width=200, height=50)

AvaBtt = Button(frame4, text="Update account", font=("Roboto", 14, "bold"), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:updateaccount())
AvaBtt.place(x = 537, y = 540, width=200, height=50)

bts_btt1 = Button(frame4, image=bts, borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:show_frame(frame3))
bts_btt1.place(x = 10, y = 680)

#===================================================Book Search Screen
sebg = PhotoImage(file = "Search_BG.png")
search_bg = Label(frame5, image = sebg)
search_bg.place(x = -2,y = -2)


results_bg2 = Frame(frame5, bg = "#f4f4f8")
results_bg2.place(x = 580, y = 0 , width = 700, height = 720)

results_bg1 = Frame(frame5, bg = "#f4f4f8")
results_bg1.place(x = 580, y = 0 , width = 700, height = 720)

results_bg1.lift()

s = StringVar()
s.set('Search...')
Search_Bar = ttk.Combobox(frame5, textvariable=s, font=("Roboto", 16), foreground="White")
Search_Bar.place(x = 30, y = 250, width= 475, height=43)
l = StringVar()
l.set("bookname")


Search_Bar['values'] = ('Life Science (Holt Science And Technology)', 'Macbeth', 'Haese maths book 7', 'Haese maths book 9', 'Haese maths book 8')


searchbt = Button(frame5, text="Search", font=("Roboto", 15), bg ="#2AB7CA", fg="White", borderwidth=0, command=lambda:showresults())
searchbt.place(x = 30, y = 300, width = 100, height = 40)

bts_btt2 = Button(frame5, image=bts, borderwidth=0, highlightthickness = 0, bd = 0, activebackground="#FE8D56", command=lambda:show_frame(frame3))
bts_btt2.place(x = 10, y = 680)







#===========================================END
show_frame(frame1)
root.resizable(False, False)
root.mainloop()

