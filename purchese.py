from pythondb import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

comboSupplier=""
comboItem=""
varPurchNum=""
varQuantity=""
varRate=""
varTotal=""

def LoadPurchNumber():
    global  rsPurchNum , con , curData , varPurchNum
    sql = "select max(PurchNumber) from PurchaseMain"
    mycursor = con.cursor()
    mycursor.execute(sql);
    rsPurchNum = mycursor.fetchone()
    if rsPurchNum[0]==None:
        pid = 1
    else:
        pid = int(rsPurchNum[0]) + 1
    varPurchNum.set(pid)

def LoadSupplierName():
    global rsSupplierName, curData, con, comboSupplier, lstSupplier
    sql = "select * from suppliersDetails order by supplierName"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsSupplierName = mycursor.fetchall()
    lstSupplier=[]
    for row in rsSupplierName:
        lstSupplier.append(row[1])
    curData = 0
    comboSupplier["values"]=lstSupplier

def GetSupplierDetail(self):
    global rsSupplierName, varAddress, varBalance
    varAddress.set(rsSupplierName[comboSupplier.current()][2])
    varBalance.set(rsSupplierName[comboSupplier.current()][5])

def LoadItemName():
    global rsItemName, curData, con, comboItem, lstItem
    sql = "select * from ItemsDetails order by ItemName"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsItemName = mycursor.fetchall()
    lstItem=[]
    for row in rsItemName:
        lstItem.append(row[1])
    curData = 0
    comboItem["values"]=lstItem

def getTotal():
    global tree
    totl = 0
    sn = 0
    for itm in tree.get_children():
        sn = int(sn)+1
        totl = totl + int(tree.item(itm)["values"][4])
        row = tree.item(itm)["values"]
        row[0] = sn
        tree.item( itm, values= (row) )
    varTotal.set(totl)

def AddItemInTable():
    global varQuantity, varRate, varTotal, tree
    nam = comboItem.get()
    qnty = varQuantity.get()
    rate = varRate.get()
    amnt = qnty * rate
    sn = len( tree.get_children() ) + 1
    tree.insert("", END, values=[sn, nam, qnty, rate, amnt])
    getTotal()

def RemoveItemFromTable():
    global tree
    all = tree.selection()
    for one in all:
        tree.delete(one)
    getTotal()

def SaveData():
    global txtcomboDate, txtcomboMonth, txtcomboYear, tree
    global rsSupplierName, varPurchNum, varRemark
    global con
    txtDateString = txtcomboDate.get() + "-" + txtcomboMonth.get() + "-" + txtcomboYear.get()
    supplierID = rsSupplierName[comboSupplier.current()][0]

    sql00 = "select supplierCurrAmount from suppliersDetails where Id='{}'".format(supplierID)
    mycursor = con.cursor()
    mycursor.execute(sql00)
    supplierCurAmnt = mycursor.fetchone()

    sql01 = "insert into PurchaseMain(PurchNumber,PurchDate,SupplierId,TotalAmount,Remark) values('{}','{}','{}','{}','{}')".format(varPurchNum.get(),txtDateString ,supplierID ,varTotal.get() ,varRemark.get())
    sql02 = "update suppliersDetails SET supplierCurrAmount = '{}'+'{}' where Id='{}' ".format(supplierCurAmnt[0],varTotal.get(),supplierID)
    mycursor = con.cursor()
    mycursor.execute(sql01)
    mycursor.execute(sql02)
    con.commit()

    for itm in tree.get_children():
        row = tree.item(itm)["values"]

        sql = "select CurrQuantity from ItemsDetails where ItemName='{}'".format(row[1])
        mycursor = con.cursor()
        mycursor.execute(sql)
        CurQnt = mycursor.fetchone()

        sql1 = "insert into PurchaseDetails(RefPurchNumber,RefSupplierId,ItemName,ItemQuantity,ItemRate,Amount) values('{}','{}','{}','{}','{}','{}')".format(varPurchNum.get() , supplierID, row[1], row[2], row[3], row[4])
        sql2 = "update ItemsDetails SET CurrQuantity = '{}'+'{}' where ItemName='{}'".format(CurQnt[0],row[2],row[1])
        mycursor = con.cursor()
        mycursor.execute(sql1)
        mycursor.execute(sql2)
        con.commit()
    messagebox.showinfo("Successful !", "Data has been Added to the Database.", parent=purch)

def exiting():
    global purch
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Exit..?", parent=purch)
    if x == True:
        purch.destroy()

def PurcheseDetail(root):
    global comboSupplier, comboItem, tree, lstYear
    global varPurchNum, varQuantity, varRate, varTotal, varRemark, varAddress, varBalance
    global txtcomboDate, txtcomboMonth, txtcomboYear, txtRemark , purch
    purch = Toplevel(root)
    varPurchNum = IntVar()
    varQuantity = IntVar()
    varRate = IntVar()
    varTotal = IntVar()
    varRemark = StringVar()
    varAddress = StringVar()
    varBalance = IntVar()

    Label(purch, text="Purchese Number: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=20, y=45)
    txtPurchNum = Entry(purch, textvariable=varPurchNum, width=18,state=DISABLED)
    txtPurchNum.place(x=175, y=50)

    LoadPurchNumber()

    Label(purch, text="Purchese Date: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=20, y=90)
    txtcomboDate = ttk.Combobox(purch, width=4)
    txtcomboDate.place(x=155, y=95)
    txtcomboMonth = ttk.Combobox(purch, width=5)
    txtcomboMonth.place(x=205, y=95)
    txtcomboYear = ttk.Combobox(purch, width=7)
    txtcomboYear.place(x=260, y=95)

    lstDate = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    lstMonth = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sept","Oct","Nov","Dec"]
    lstYear = []
    for i in range(2000,2023):
        lstYear.append(i);
    txtcomboDate["values"] = lstDate
    txtcomboMonth["values"] = lstMonth
    txtcomboYear["values"] = lstYear

    Label(purch, text="Supplier Name : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=400, y=25)
    comboSupplier = ttk.Combobox(purch, width=25)
    comboSupplier.place(x=550, y=28)
    comboSupplier.bind("<<ComboboxSelected>>", GetSupplierDetail)

    LoadSupplierName()

    Label(purch, text="Address : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=405, y=70)
    supplierAdd = Entry(purch, width=28, textvariable=varAddress)
    supplierAdd.place(x=550, y=73)

    Label(purch, text="Balance : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=405, y=115)
    Balance = Entry(purch, width=28, textvariable=varBalance)
    Balance.place(x=550, y=118)

    Label(purch, text="Item Name: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=10, y=200)
    comboItem = ttk.Combobox(purch, width=18)
    comboItem.place(x=115, y=203)

    LoadItemName()

    Label(purch, text="Quantity: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=255, y=200)
    purchQnty = Entry(purch, textvariable=varQuantity, width=15).place(x=345, y=205)

    Label(purch, text="Rate: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=450, y=200)
    purchRate = Entry(purch, textvariable=varRate, width=15).place(x=510, y=205)

    Button(purch, text="Add Item", width="11", bg="green", fg="white", font=("consolas", 8,"bold"),command=AddItemInTable).place(x=620, y=203)
    Button(purch, text="Remove Item", width="11", bg="red", fg="white", font=("consolas", 8,"bold"),command=RemoveItemFromTable).place(x=700, y=203)

    columns = ('col1', 'col2', 'col3', 'col4', 'col5')
    tree = ttk.Treeview(purch, columns=columns, show='headings')
    tree.heading('col1', text='S.No.')
    tree.heading('col2', text='Item Name')
    tree.heading('col3', text='Quantity')
    tree.heading('col4', text='Rate')
    tree.heading('col5', text='Amount')

    tree.column("col1", width=40)
    tree.column("col2", width=140)
    tree.column("col3", width=100)
    tree.column("col4", width=100)
    tree.column("col5", width=140)

    tree.place(x=20, y=250)

    Label(purch, text="Remark : ", bg="#ffcccc", font=("consolas", 14,"bold")).place(x=560, y=320)
    txtRemark = Entry(purch, width=35,textvariable=varRemark).place(x=560, y=350)

    Button(purch, text="Save", width="12", bg="green", fg="white", font=("consolas", 10,"bold"),command=SaveData).place(x=60, y=505)
    Button(purch, text="Cancel", width="12", bg="red", fg="white", font=("consolas", 10,"bold"),command=exiting).place(x=190, y=505)

    Label(purch, text="Total : ", bg="#ffcccc", font=("consolas", 14,"bold")).place(x=555, y=505)
    total = Entry(purch, textvariable=varTotal, width=18).place(x=640, y=510)

    purch.title("Purchese Screen")
    purch.config(bg="#ffcccc")
    purch.geometry("800x550+250+80")
    purch.mainloop()


#PurcheseDetail()