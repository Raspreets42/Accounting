from pythondb import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

curId=0
saveFlag=False
findflag=False
rsItem=""
curData=0

def componentEnableDisable(flag):
    global custoName , custoAdd,  custoMob , custoAmount
    global Firstbtn , Nextbtn , Prevbtn , Lastbtn
    global Addbtn , Savebtn , Editbtn , Findbtn , Deletebtn , Cancelbtn
    if flag==True:
        st=NORMAL
        st1=DISABLED
    else:
        st=DISABLED
        st1=NORMAL
        
    custoName.config(state=st)
    custoAdd.config(state=st)
    custoMob.config(state=st)
    custoAmount.config(state=st)
    
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
    custoName.delete(0,END)
    custoAdd.delete(0, END)
    custoMob.delete(0, END)
    custoAmount.delete(0, END)
    custoName.focus_set()
    saveFlag=True

def editData():
    global saveFlag
    componentEnableDisable(True)
    saveFlag=False

def saveData():
    global saveFlag
    global CustomerName , CustomerAddress , CustomerMobile , CustomerAmount
    global con , custo
    if saveFlag==True:
        if CustomerName!="" or CustomerAddress!="" or CustomerMobile!="" or CustomerAmount!="":
            sql = "insert into customersDetails(CustomerName,CustomerAddress,CustomerMobile,CustomerAmount,CustomerCurrAmount) values('{}','{}','{}','{}','{}','{}')".format(CustomerName.get(),CustomerAddress.get(),CustomerMobile.get(),CustomerAmount.get(),CustomerAmount.get())
            mycursor = con.cursor()
            mycursor.execute(sql)
            con.commit()
            messagebox.showinfo("Successful !" , "Data has been Added to the Database.", parent=custo)
        else:
            messagebox.showinfo("Warning !" , "Please Fill the Entries first before saving.")
    else:
        sql = "update customersDetails set CustomerName='{}' , CustomerAddress='{}' , CustomerMobile='{}' , CustomerAmount='{}' where id={}".format(CustomerName.get(),CustomerAddress.get(),CustomerMobile.get(),CustomerAmount.get(),curId)
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo("Successful !" , "Data has been Updated.", parent=custo)
    LoadData()
    componentEnableDisable(False)

def findData():
    global con,rsItem,curData,custo,curId
    x = simpledialog.askinteger("Accounting and Inventory" , "Enter the customer ID :", parent=custo)
    cnt=0
    for itm in rsItem:
        if itm[0]==x:
            curData=cnt
            findflag=True
            break
        else:
            findflag = False
        cnt=cnt+1
    if findflag==False:
        messagebox.showinfo("Accounting and Inventory","Customer Not Present",parent=custo)
    else:
        displayData(curData)

def deleteData():
    global con , custo,curId
    x = messagebox.askyesno("Accounting and Inventory" , "Do You really want to Delete..?", parent=custo)
    if x == True:
        sql = "delete from customersDetails where id={}".format(curId)
        print(curId)
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo("Successful !" , "Data has been Deleted to the Database.", parent=custo)
        LoadData()

def exiting():
    global custo
    x = messagebox.askyesno("Accounting and Inventory" , "Do You really want to Exit..?", parent=custo)
    if x == True:
        custo.destroy()
        
def displayData(r):
    global CustomerName , CustomerAddress , CustomerMobile , CustomerAmount
    global rsItem, curId
    curId = rsItem[r][0]
    CustomerName.set(rsItem[r][1])
    CustomerAddress.set(rsItem[r][2])
    CustomerMobile.set(rsItem[r][3])
    CustomerAmount.set(rsItem[r][4])

def Lastdatabtn():
    global curData,rsItem
    componentEnableDisable(False)
    curData=len(rsItem)-1
    displayData(curData)

def Nextdatabtn():
    global curData,rsItem, custo
    componentEnableDisable(False)
    if curData < len(rsItem)-1:
        curData = curData + 1
        displayData(curData)
    else:
        messagebox.showinfo("Sensible","It is last record", parent=custo)

def Prevdatabtn():
    global curData,rsItem, custo
    componentEnableDisable(False)
    if curData > 0:
        curData = curData - 1
        displayData(curData)
    else:
        messagebox.showinfo("Sensible","It is first record", parent=custo)

def Firstdatabtn():
    global curData
    componentEnableDisable(False)
    curData=0
    displayData(curData)

def LoadData():
    global rsItem, curData, con
    sql = "select * from customersDetails"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsItem = mycursor.fetchall()
    curData=0
    displayData(curData)

def customerDetail(root):

    global custo
    custo = Toplevel(root)
    
    global CustomerName , CustomerAddress , CustomerMobile , CustomerAmount , CustomerAmoutType
    global custoName , custoAdd,  custoMob , custoAmount
    global Firstbtn , Nextbtn , Prevbtn , Lastbtn
    global Addbtn , Savebtn , Editbtn , Findbtn , Deletebtn , Cancelbtn
    CustomerName = StringVar()
    CustomerAddress = StringVar()
    CustomerMobile = StringVar()
    CustomerAmount = IntVar()

    custo.title("Customer Screen")
    custo.config(bg="#ffcccc")

    Label(custo, text="Customer Name : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=20) #x=x+110
    custoName = Entry(custo, textvariable=CustomerName, width=50,state=DISABLED)
    custoName.place(x=280, y=25) #x=x+120

    Label(custo, text="Address : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=60)
    custoAdd = Entry(custo, textvariable=CustomerAddress, width=50,state=DISABLED)
    custoAdd.place(x=280, y=65)

    Label(custo, text="Mobile No. : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=100)
    custoMob = Entry(custo, textvariable=CustomerMobile, width=50,state=DISABLED)
    custoMob.place(x=280, y=105)

    Label(custo, text="Opening Amount : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=140)
    custoAmount = Entry(custo, textvariable=CustomerAmount, width=50,state=DISABLED)
    custoAmount.place(x=280, y=145)

    #Label(custo, text="Opening Type : ", bg="#ffcccc", font=("consolas", 12)).place(x=120, y=180)
    #Radiobutton(custo, text="Lendari", bg="#ffcccc", variable=var, value="Lendari").place(x=280, y=182)
    #Radiobutton(custo, text="Dendari", bg="#ffcccc", variable=var, value="Dendari").place(x=380, y=182)

    Firstbtn = Button(custo, text="<<", width="10", bg="black", fg="white", command=Firstdatabtn)
    Firstbtn.place(x=130, y=240)
    Prevbtn = Button(custo, text="<", width="10", bg="black", fg="white", command=Prevdatabtn)
    Prevbtn.place(x=250, y=240)
    Nextbtn = Button(custo, text=">", width="10", bg="black", fg="white", command=Nextdatabtn)
    Nextbtn.place(x=370, y=240)
    Lastbtn = Button(custo, text=">>", width="10", bg="black", fg="white", command=Lastdatabtn)
    Lastbtn.place(x=490, y=240)

    Addbtn = Button(custo, text="Add", width="15", bg="green", fg="white", command= addData)
    Addbtn.place(x=140, y=280)
    Savebtn = Button(custo, text="Save", width="15", bg="green", fg="white", state=DISABLED, command= saveData)
    Savebtn.place(x=300, y=280)
    Cancelbtn = Button(custo, text="Cancel", width="15", bg="green", fg="white", state=DISABLED, command=cancelOperation)
    Cancelbtn.place(x=450, y=280)
    Editbtn = Button(custo, text="Edit", width="15", bg="red", fg="white", command= editData)
    Editbtn.place(x=140, y=320)
    Findbtn = Button(custo, text="Find", width="15", bg="red", fg="white", command= findData)
    Findbtn.place(x=300, y=320)
    Deletebtn = Button(custo, text="Delete", width="15", bg="red", fg="white", command= deleteData)
    Deletebtn.place(x=450, y=320)
    
    Button(custo, text="Exit", width="40", bg="black", fg="white", command=exiting).place(x=210, y=360)

    LoadData()

    custo.geometry("700x500+300+100")
    custo.mainloop()

#customerDetail()
