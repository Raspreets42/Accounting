from pythondb import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

curId = 0
saveFlag = False
findflag = False
rsItem = ""
curData = 0


def componentEnableDisable(flag):
    global itmName, itmQyantity
    global Firstbtn, Nextbtn, Prevbtn, Lastbtn
    global Addbtn, Savebtn, Editbtn, Findbtn, Deletebtn, Cancelbtn
    if flag == True:
        st = NORMAL
        st1 = DISABLED
    else:
        st = DISABLED
        st1 = NORMAL

    itmName.config(state=st)
    itmQuantity.config(state=st)

    Firstbtn.config(state=st1)
    Prevbtn.config(state=st1)
    Nextbtn.config(state=st1)
    Lastbtn.config(state=st1)

    Addbtn.config(state=st1)
    Savebtn.config(state=st)
    Cancelbtn.config(state=st)
    Editbtn.config(state=st1)
    Findbtn.config(state=st1)
    Deletebtn.config(state=st1)


def cancelOperation():
    componentEnableDisable(False)


def addData():
    global saveFlag
    componentEnableDisable(True)
    itmName.delete(0, END)
    itmQuantity.delete(0, END)
    itmName.focus_set()
    saveFlag = True


def editData():
    global saveFlag
    componentEnableDisable(True)
    saveFlag = False


def saveData():
    global saveFlag
    global ItemName, ItemQuantity
    global con, itm
    if saveFlag == True:
        if ItemName != "" or ItemQuantity != "":
            sql = "insert into ItemsDetails(ItemName,ItemQuantity,CurrQuantity) values('{}','{}','{}')".format(
                ItemName.get(), ItemQuantity.get(), ItemQuantity.get())
            mycursor = con.cursor()
            mycursor.execute(sql)
            con.commit()
            messagebox.showinfo("Successful !", "Data has been Added to the Database.", parent=itm)
        else:
            messagebox.showinfo("Warning !", "Please Fill the Entries first before saving.")
    else:
        sql = "update ItemsDetails set ItemName='{}' , ItemQuantity='{}',   where id={}".format(ItemName.get(), ItemQuantity.get(), curId)
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo("Successful !", "Data has been Updated.", parent=itm)
    LoadData()
    componentEnableDisable(False)


def findData():
    global con, rsItem, curData, itm, curId
    x = simpledialog.askinteger("Accounting and Inventory", "Enter the Item ID :", parent=itm)
    cnt = 0
    for itmm in rsItem:
        if itmm[0] == x:
            curData = cnt
            findflag = True
            break
        else:
            findflag = False
        cnt = cnt + 1
    if findflag == False:
        messagebox.showinfo("Accounting and Inventory", "Item Not Present", parent=itm)
    else:
        displayData(curData)

def deleteData():
    global con, itm, curId
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Delete..?", parent=itm)
    if x == True:
        sql = "delete from ItemsDetails where id={}".format(curId)
        print(curId)
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo("Successful !", "Data has been Deleted to the Database.", parent=itm)
        LoadData()


def exiting():
    global itm
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Exit..?", parent=itm)
    if x == True:
        itm.destroy()


def displayData(r):
    global ItemName, ItemQuantity
    global rsItem, curId
    curId = rsItem[r][0]
    ItemName.set(rsItem[r][1])
    ItemQuantity.set(rsItem[r][2])


def Lastdatabtn():
    global curData, rsItem
    componentEnableDisable(False)
    curData = len(rsItem) - 1
    displayData(curData)


def Nextdatabtn():
    global curData, rsItem, itm
    componentEnableDisable(False)
    if curData < len(rsItem) - 1:
        curData = curData + 1
        displayData(curData)
    else:
        messagebox.showinfo("Sensible", "It is last record", parent=itm)


def Prevdatabtn():
    global curData, rsItem, itm
    componentEnableDisable(False)
    if curData > 0:
        curData = curData - 1
        displayData(curData)
    else:
        messagebox.showinfo("Sensible", "It is first record", parent=itm)


def Firstdatabtn():
    global curData
    componentEnableDisable(False)
    curData = 0
    displayData(curData)


def LoadData():
    global rsItem, curData, con
    sql = "select * from ItemsDetails"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsItem = mycursor.fetchall()
    curData = 0
    displayData(curData)


def ItemDetail(root):
    global itm
    itm = Toplevel(root)

    global ItemName, ItemQuantity
    global itmName, itmQuantity
    global Firstbtn, Nextbtn, Prevbtn, Lastbtn
    global Addbtn, Savebtn, Editbtn, Findbtn, Deletebtn, Cancelbtn
    ItemName = StringVar()
    ItemQuantity = IntVar()

    itm.title("Item Screen")
    itm.config(bg="#ffcccc")

    Label(itm, text="item Name : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=50)
    itmName = Entry(itm, textvariable=ItemName, width=50, state=DISABLED)
    itmName.place(x=280, y=55)

    Label(itm, text="Item Quantity : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=110)
    itmQuantity = Entry(itm, textvariable=ItemQuantity, width=50, state=DISABLED)
    itmQuantity.place(x=280, y=115)

    Firstbtn = Button(itm, text="<<", width="10", bg="black", fg="white", command=Firstdatabtn)
    Firstbtn.place(x=130, y=210)
    Prevbtn = Button(itm, text="<", width="10", bg="black", fg="white", command=Prevdatabtn)
    Prevbtn.place(x=250, y=210)
    Nextbtn = Button(itm, text=">", width="10", bg="black", fg="white", command=Nextdatabtn)
    Nextbtn.place(x=370, y=210)
    Lastbtn = Button(itm, text=">>", width="10", bg="black", fg="white", command=Lastdatabtn)
    Lastbtn.place(x=490, y=210)

    Addbtn = Button(itm, text="Add", width="15", bg="green", fg="white", command=addData)
    Addbtn.place(x=140, y=260)
    Savebtn = Button(itm, text="Save", width="15", bg="green", fg="white", state=DISABLED, command=saveData)
    Savebtn.place(x=300, y=260)
    Cancelbtn = Button(itm, text="Cancel", width="15", bg="green", fg="white", state=DISABLED,
                       command=cancelOperation)
    Cancelbtn.place(x=450, y=260)
    Editbtn = Button(itm, text="Edit", width="15", bg="red", fg="white", command=editData)
    Editbtn.place(x=140, y=310)
    Findbtn = Button(itm, text="Find", width="15", bg="red", fg="white", command=findData)
    Findbtn.place(x=300, y=310)
    Deletebtn = Button(itm, text="Delete", width="15", bg="red", fg="white", command=deleteData)
    Deletebtn.place(x=450, y=310)

    Button(itm, text="Exit", width="40", bg="black", fg="white", command=exiting).place(x=210, y=360)

    LoadData()

    itm.geometry("700x500+300+100")
    itm.mainloop()

#ItemDetail()
