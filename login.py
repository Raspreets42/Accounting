from pythondb import *
from menubar import *
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk  #pip install pillow <- command prompt

def Inn():
    global Username, Password
    global top
    sql = "select * from logins where Username='{}'".format(Username.get())
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsUser = mycursor.fetchone()
    if rsUser:
        if rsUser[1] == Username.get() :
            if rsUser[2] == Password.get():
                menubar(top)
            else:
                messagebox.showerror("Warning !", "Invalid Password")
        else:
            messagebox.showerror("Warning !", "Invalid Username")
    else:
        messagebox.showerror("Warning !" , "Please Fill the Username and Password")

global Username, Password
global top
top = Tk()
Username = StringVar()
Password = StringVar()
top.title("Login Screen")
bg = ImageTk.PhotoImage(file="loginimg.jpg")
labelI = Label(top , image = bg).place(x=0,y=0,relwidth=1,relheight=1)

login_frame = Frame(top,bg="#ffe6e6").place(x=95,y=10,height=100,width=500)

Label(login_frame, text="UserName : ", bg="#ffe6e6", font=("consolas", 15,"bold")).place(x=105,y=15)
inputuser = Entry(login_frame, textvariable=Username, width=50).place(x=255,y=21)

Label(login_frame, text="Password : ", bg="#ffe6e6", font=("consolas", 15,"bold")).place(x=105,y=60)
inputpassword = Entry(login_frame, textvariable=Password, show="*", width=50).place(x=255,y=66)

loginbtn = Button(top, text="Login", width="15", bg="#80ff00", command=Inn).place(x=290,y=100)

top.geometry("700x500+300+100")
top.resizable(False,False)
top.mainloop()
