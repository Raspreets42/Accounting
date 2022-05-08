from pythondb import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

comboCustomer=""
comboItem=""
varSaleNum=""
varQuantity=""
varRate=""
varTotal=""

def LoadSaleNumber():
    global  rsSaleNum , con , curData , varSaleNum
    sql = "select max(SaleNumber) from SalesMain"
    mycursor = con.cursor()
    mycursor.execute(sql);
    rsSaleNum = mycursor.fetchone()
    if rsSaleNum[0]==None:
        sid = 1
    else:
        sid = int(rsSaleNum[0]) + 1
    varSaleNum.set(sid)

def LoadCustomerName():
    global rsCustomerName, curData, con, comboCustomer, lstCustomer
    sql = "select * from customersDetails order by customerName"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsCustomerName = mycursor.fetchall()
    lstCustomer=[]
    for row in rsCustomerName:
        lstCustomer.append(row[1])
    curData = 0
    comboCustomer["values"]=lstCustomer

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


def GetCustomerDetail(self):
    global rsCustomerName, varAddress, varBalance
    varAddress.set(rsCustomerName[comboCustomer.current()][2])
    varBalance.set(rsCustomerName[comboCustomer.current()][5])

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
    global rsCustomerName, varSaleNum, varRemark
    global con
    txtDateString = txtcomboDate.get() + "-" + txtcomboMonth.get() + "-" + txtcomboYear.get()
    CustomerID = rsCustomerName[comboCustomer.current()][0]


    sql00 = "select CustomerCurrAmount from CustomersDetails where id='{}'".format(CustomerID)
    mycursor = con.cursor()
    mycursor.execute(sql00)
    customerCurAmnt = mycursor.fetchone()

    sql01 = "insert into SalesMain(SaleNumber,SalesDate,CustomerId,TotalAmount,Remark) values('{}','{}','{}','{}','{}')".format(varSaleNum.get(),txtDateString ,CustomerID ,varTotal.get() ,varRemark.get())
    sql02 = "update CustomersDetails SET CustomerCurrAmount = '{}'+'{}' where id='{}' ".format(customerCurAmnt[0],varTotal.get(),CustomerID)
    mycursor = con.cursor()
    mycursor.execute(sql01)
    mycursor.execute(sql02)
    con.commit()

    for itm in tree.get_children():
        row = tree.item(itm)["values"]

        sql0 = "select CurrQuantity from ItemsDetails where ItemName='{}'".format(row[1])
        mycursor = con.cursor()
        mycursor.execute(sql0)
        CurQnt = mycursor.fetchone()

        sql1 = "insert into SalesDetails(RefSaleNumber,RefcustomerId,ItemName,ItemQuantity,ItemRate,Amount) values('{}','{}','{}','{}','{}','{}')".format(varSaleNum.get() , CustomerID, row[1], row[2], row[3], row[4])
        sql2 = "update ItemsDetails SET CurrQuantity = '{}'-'{}' where ItemName='{}'".format(CurQnt[0], row[2], row[1])
        mycursor = con.cursor()
        mycursor.execute(sql1)
        mycursor.execute(sql2)
        con.commit()

    messagebox.showinfo("Successful !", "Data has been Added to the Database.", parent=sale)

def exiting():
    global sale
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Exit..?", parent=sale)
    if x == True:
        sale.destroy()

def SalesDetail(root):
    global comboCustomer, comboItem, tree, lstYear
    global varSaleNum, varQuantity, varRate, varTotal, varRemark, varAddress, varBalance
    global txtcomboDate, txtcomboMonth, txtcomboYear, txtRemark , sale
    sale = Toplevel(root)
    varSaleNum = IntVar()
    varQuantity = IntVar()
    varRate = IntVar()
    varTotal = IntVar()
    varRemark = StringVar()
    varAddress = StringVar()
    varBalance = IntVar()

    Label(sale, text="Sales Number: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=20, y=45)
    txtSaleNum = Entry(sale, textvariable=varSaleNum, width=18,state=DISABLED)
    txtSaleNum.place(x=175, y=50)

    LoadSaleNumber()

    Label(sale, text="Sales Date: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=20, y=90)
    txtcomboDate = ttk.Combobox(sale, width=4)
    txtcomboDate.place(x=155, y=95)
    txtcomboMonth = ttk.Combobox(sale, width=5)
    txtcomboMonth.place(x=205, y=95)
    txtcomboYear = ttk.Combobox(sale, width=7)
    txtcomboYear.place(x=260, y=95)

    lstDate = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    lstMonth = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sept","Oct","Nov","Dec"]
    lstYear = []
    for i in range(2000,2023):
        lstYear.append(i);
    txtcomboDate["values"] = lstDate
    txtcomboMonth["values"] = lstMonth
    txtcomboYear["values"] = lstYear

    Label(sale, text="Customer Name : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=400, y=25)
    comboCustomer = ttk.Combobox(sale, width=25)
    comboCustomer.place(x=550, y=28)
    comboCustomer.bind("<<ComboboxSelected>>", GetCustomerDetail)

    LoadCustomerName()

    Label(sale, text="Address : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=405, y=70)
    customerAdd = Entry(sale, width=28, textvariable= varAddress)
    customerAdd.place(x=550, y=73)

    Label(sale, text="Balance : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=405, y=115)
    Balance = Entry(sale, width=28, textvariable= varBalance)
    Balance.place(x=550, y=118)

    Label(sale, text="Item Name: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=10, y=200)
    comboItem = ttk.Combobox(sale, width=18)
    comboItem.place(x=115, y=203)

    LoadItemName()

    Label(sale, text="Quantity: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=255, y=200)
    purchQnty = Entry(sale, textvariable=varQuantity, width=15).place(x=345, y=205)

    Label(sale, text="Rate: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=450, y=200)
    purchRate = Entry(sale, textvariable=varRate, width=15).place(x=510, y=205)

    Button(sale, text="Add Item", width="11", bg="green", fg="white", font=("consolas", 8,"bold"),command=AddItemInTable).place(x=620, y=203)
    Button(sale, text="Remove Item", width="11", bg="red", fg="white", font=("consolas", 8,"bold"),command=RemoveItemFromTable).place(x=700, y=203)

    columns = ('col1', 'col2', 'col3', 'col4', 'col5')
    tree = ttk.Treeview(sale, columns=columns, show='headings')
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

    Label(sale, text="Remark : ", bg="#ffcccc", font=("consolas", 14,"bold")).place(x=560, y=320)
    txtRemark = Entry(sale, width=35,textvariable=varRemark).place(x=560, y=350)

    Button(sale, text="Save", width="12", bg="green", fg="white", font=("consolas", 10,"bold"),command=SaveData).place(x=60, y=505)
    Button(sale, text="Cancel", width="12", bg="red", fg="white", font=("consolas", 10,"bold"),command=exiting).place(x=190, y=505)

    Label(sale, text="Total : ", bg="#ffcccc", font=("consolas", 14,"bold")).place(x=555, y=505)
    total = Entry(sale, textvariable=varTotal, width=18).place(x=640, y=510)

    sale.title("Sales Screen")
    sale.config(bg="#ffcccc")
    sale.geometry("800x550+250+80")
    sale.mainloop()


#SalesDetail()