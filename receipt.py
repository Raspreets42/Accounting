from pythondb import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def LoadCustomerName():
    global rsCustomerName, curData, con, comboCustomer, lstCustomer
    sql = "select * from customersDetails order by CustomerName"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsCustomerName = mycursor.fetchall()
    lstCustomer = []
    for row in rsCustomerName:
        lstCustomer.append(row[1])
    curData = 0
    comboCustomer["values"] = lstCustomer

def GetCustomerDetail(self):
    global rsCustomerName, varAddress, varBalance
    varAddress.set(rsCustomerName[comboCustomer.current()][2])
    varBalance.set(rsCustomerName[comboCustomer.current()][5])

def SaveData():
    global txtcomboDate, txtcomboMonth, txtcomboYear
    global rsCustomerName, varAmount, varRemark
    global con, recpt
    txtDateString = txtcomboDate.get() + "-" + txtcomboMonth.get() + "-" + txtcomboYear.get()
    customerID = rsCustomerName[comboCustomer.current()][0]

    sql00 = "select CustomerCurrAmount from CustomersDetails where id='{}'".format(customerID)
    mycursor = con.cursor()
    mycursor.execute(sql00)
    customerCurAmnt = mycursor.fetchone()

    sql01 = "insert into ReceiptInformation(CustomerId,ReceiptDate,Amount,Remark) values('{}','{}','{}','{}')".format(customerID, txtDateString, varAmount.get(), varRemark.get())
    sql02 = "update CustomersDetails SET CustomerCurrAmount = '{}'-'{}' where id='{}' ".format(customerCurAmnt[0],varAmount.get(),customerID)
    mycursor = con.cursor()
    mycursor.execute(sql01)
    mycursor.execute(sql02)
    con.commit()
    messagebox.showinfo("Successful !", "Data has been Added to the Database.", parent=recpt)


def Exiting():
    global recpt
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Exit..?", parent=recpt)
    if x == True:
        recpt.destroy()

def ReceiptDetail(root):
    global recpt, comboCustomer, varAmount, varRemark, varAddress, varBalance
    global txtcomboDate, txtcomboMonth, txtcomboYear

    recpt = Toplevel(root)

    varAmount = IntVar()
    varRemark = StringVar()
    varAddress = StringVar()
    varBalance = IntVar()

    Label(recpt, text="Customer Name: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=30)
    comboCustomer = ttk.Combobox(recpt, width=24)
    comboCustomer.place(x=340, y=30)
    comboCustomer.bind("<<ComboboxSelected>>", GetCustomerDetail)

    LoadCustomerName()

    Label(recpt, text="Address: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=80)
    customerAdd = Entry(recpt, width=27, textvariable=varAddress).place(x=340, y=85)

    Label(recpt, text="Balance : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=130)
    txtBalance = Entry(recpt, width=27, textvariable=varBalance).place(x=340, y=135)

    Label(recpt, text="Receipt Date : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=180)
    txtcomboDate = ttk.Combobox(recpt, width=4)
    txtcomboDate.place(x=340, y=185)
    txtcomboMonth = ttk.Combobox(recpt, width=5)
    txtcomboMonth.place(x=390, y=185)
    txtcomboYear = ttk.Combobox(recpt, width=6)
    txtcomboYear.place(x=445, y=185)

    lstDate = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
               "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
    lstMonth = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    lstYear = []
    for i in range(2000, 2023):
        lstYear.append(i);
    txtcomboDate["values"] = lstDate
    txtcomboMonth["values"] = lstMonth
    txtcomboYear["values"] = lstYear

    Label(recpt, text="Amount : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=230)
    txtAmount = Entry(recpt, width=27, textvariable=varAmount).place(x=340, y=235)

    Label(recpt, text="Remark : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=280)
    txtRemark = Entry(recpt, width=27, textvariable=varRemark).place(x=340, y=285)

    Button(recpt, text=" Ok ", width="11", bg="green", fg="white", font=("consolas", 9,"bold"), command=SaveData ).place(x=240, y=350)
    Button(recpt, text="Cancel", width="11", bg="red", fg="white", font=("consolas", 9,"bold"), command=Exiting ).place(x=370, y=350)

    recpt.title("Receipts Screen")
    recpt.config(bg="#ffcccc")
    recpt.geometry("700x500+300+100")
    recpt.mainloop()

#ReceiptDetail()