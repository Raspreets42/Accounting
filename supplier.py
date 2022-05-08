from pythondb import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

curId = 0
saveFlag = False
findflag=False
rsItem = ""
curData = 0

def componentEnableDisable(flag):
    global supName, supAdd, supMob, supAmount
    global Firstbtn, Nextbtn, Prevbtn, Lastbtn
    global Addbtn, Savebtn, Editbtn, Findbtn, Deletebtn, Cancelbtn
    if flag == True:
        st = NORMAL
        st1 = DISABLED
    else:
        st = DISABLED
        st1 = NORMAL

    supName.config(state=st)
    supAdd.config(state=st)
    supMob.config(state=st)
    supAmount.config(state=st)

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
    supName.delete(0, END)
    supAdd.delete(0, END)
    supMob.delete(0, END)
    supAmount.delete(0, END)
    supName.focus_set()
    saveFlag = True

def editData():
    global saveFlag
    componentEnableDisable(True)
    saveFlag = False

def saveData():
    global saveFlag
    global supplierName, supplierAddress, supplierMobile, supplierAmount, var
    global con, sup
    if saveFlag == True:
        if supplierName != "" or supplierAddress != "" or supplierMobile != "" or supplierAmount != "":
            sql = "insert into suppliersDetails(supplierName,supplierAddress,supplierMobile,supplierAmount,supplierCurrAmount) values('{}','{}','{}','{}','{}','{}')".format(supplierName.get(), supplierAddress.get(), supplierMobile.get(), supplierAmount.get(), supplierAmount.get() )
            mycursor = con.cursor()
            mycursor.execute(sql)
            con.commit()
            messagebox.showinfo("Successful !", "Data has been Added to the Database.", parent=sup)
        else:
            messagebox.showinfo("Warning !", "Please Fill the Entries first before saving.")
    else:
        sql = "update suppliersDetails set supplierName='{}' , supplierAddress='{}' , supplierMobile='{}' , supplierAmount='{}' where id={}".format(supplierName.get(), supplierAddress.get(), supplierMobile.get(), supplierAmount.get(), curId)
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo("Successful !", "Data has been Updated.", parent=sup)
    LoadData()
    componentEnableDisable(False)

def findData():
    global con,rsItem,curData,sup,curId
    x = simpledialog.askinteger("Accounting and Inventory", "Enter the Supplier ID :", parent=sup)
    cnt=0
    for itm in rsItem:
        if itm[0] == x:
            curData = cnt
            findflag = True
            break
        else:
            findflag = False
        cnt = cnt+1
    if findflag == False:
        messagebox.showinfo("Accounting and Inventory", "Supplier Not Present", parent=sup)
    else:
        displayData(curData)

def deleteData():
    global con, sup, curId
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Delete..?", parent=sup)
    if x == True:
        sql = "delete from suppliersDetails where id={}".format(curId)
        print(curId)
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo("Successful !", "Data has been Deleted to the Database.", parent=sup)
        LoadData()

def exiting():
    global sup
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Exit..?", parent=sup)
    if x == True:
        sup.destroy()

def displayData(r):
    global supplierName, supplierAddress, supplierMobile, supplierAmount, var
    global rsItem, curId
    curId = rsItem[r][0]
    supplierName.set(rsItem[r][1])
    supplierAddress.set(rsItem[r][2])
    supplierMobile.set(rsItem[r][3])
    supplierAmount.set(rsItem[r][4])

def Lastdatabtn():
    global curData, rsItem
    componentEnableDisable(False)
    curData = len(rsItem) - 1
    displayData(curData)

def Nextdatabtn():
    global curData, rsItem, sup
    componentEnableDisable(False)
    if curData < len(rsItem) - 1:
        curData = curData + 1
        displayData(curData)
    else:
        messagebox.showinfo("Sensible", "It is last record", parent=sup)

def Prevdatabtn():
    global curData, rsItem, sup
    componentEnableDisable(False)
    if curData > 0:
        curData = curData - 1
        displayData(curData)
    else:
        messagebox.showinfo("Sensible", "It is first record", parent=sup)

def Firstdatabtn():
    global curData
    componentEnableDisable(False)
    curData = 0
    displayData(curData)

def LoadData():
    global rsItem, curData, con
    sql = "select * from suppliersDetails"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsItem = mycursor.fetchall()
    curData=0
    displayData(curData)


def supplierDetail(root):
    global sup
    sup = Toplevel(root)

    global supplierName, supplierAddress, supplierMobile, supplierAmount
    global supName, supAdd, supMob, supAmount
    global Firstbtn, Nextbtn, Prevbtn, Lastbtn
    global Addbtn, Savebtn, Editbtn, Findbtn, Deletebtn, Cancelbtn
    supplierName = StringVar()
    supplierAddress = StringVar()
    supplierMobile = StringVar()
    supplierAmount = IntVar()
    var = StringVar()

    sup.title("supplier Screen")
    sup.config(bg="#ffcccc")

    Label(sup, text="supplier Name : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=20)
    supName = Entry(sup, textvariable=supplierName, width=50, state=DISABLED)
    supName.place(x=280, y=25)

    Label(sup, text="Address : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=60)
    supAdd = Entry(sup, textvariable=supplierAddress, width=50, state=DISABLED)
    supAdd.place(x=280, y=65)

    Label(sup, text="Mobile No. : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=100)
    supMob = Entry(sup, textvariable=supplierMobile, width=50, state=DISABLED)
    supMob.place(x=280, y=105)

    Label(sup, text="Amount : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=140)
    supAmount = Entry(sup, textvariable=supplierAmount, width=50, state=DISABLED)
    supAmount.place(x=280, y=145)

    Firstbtn = Button(sup, text="<<", width="10", bg="black", fg="white", command=Firstdatabtn)
    Firstbtn.place(x=130, y=240)
    Prevbtn = Button(sup, text="<", width="10", bg="black", fg="white", command=Prevdatabtn)
    Prevbtn.place(x=250, y=240)
    Nextbtn = Button(sup, text=">", width="10", bg="black", fg="white", command=Nextdatabtn)
    Nextbtn.place(x=370, y=240)
    Lastbtn = Button(sup, text=">>", width="10", bg="black", fg="white", command=Lastdatabtn)
    Lastbtn.place(x=490, y=240)

    Addbtn = Button(sup, text="Add", width="15", bg="green", fg="white", command=addData)
    Addbtn.place(x=140, y=280)
    Savebtn = Button(sup, text="Save", width="15", bg="green", fg="white", state=DISABLED, command=saveData)
    Savebtn.place(x=300, y=280)
    Cancelbtn = Button(sup, text="Cancel", width="15", bg="green", fg="white", state=DISABLED,
                       command=cancelOperation)
    Cancelbtn.place(x=450, y=280)
    Editbtn = Button(sup, text="Edit", width="15", bg="red", fg="white", command=editData)
    Editbtn.place(x=140, y=320)
    Findbtn = Button(sup, text="Find", width="15", bg="red", fg="white", command=findData)
    Findbtn.place(x=300, y=320)
    Deletebtn = Button(sup, text="Delete", width="15", bg="red", fg="white", command=deleteData)
    Deletebtn.place(x=450, y=320)

    Button(sup, text="Exit", width="40", bg="black", fg="white", command=exiting).place(x=210, y=360)

    LoadData()

    sup.geometry("700x500+300+100")
    sup.mainloop()


#supplierDetail()

