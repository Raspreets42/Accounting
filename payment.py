from pythondb import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def LoadSupplierName():
    global rsSupplierName, curData, con, comboSupplier, lstSupplier
    sql = "select * from suppliersDetails order by supplierName"
    mycursor = con.cursor()
    mycursor.execute(sql)
    rsSupplierName = mycursor.fetchall()
    lstSupplier = []
    for row in rsSupplierName:
        lstSupplier.append(row[1])
    curData = 0
    comboSupplier["values"] = lstSupplier

def GetSupplierDetail(self):
    global rsSupplierName, varAddress, varBalance
    varAddress.set(rsSupplierName[comboSupplier.current()][2])
    varBalance.set(rsSupplierName[comboSupplier.current()][5])


def SaveData():
    global txtcomboDate, txtcomboMonth, txtcomboYear
    global rsSupplierName, varAmount, varRemark
    global con, pay
    txtDateString = txtcomboDate.get() + "-" + txtcomboMonth.get() + "-" + txtcomboYear.get()
    supplierID = rsSupplierName[comboSupplier.current()][0]

    sql00 = "select supplierCurrAmount from suppliersDetails where Id='{}'".format(supplierID)
    mycursor = con.cursor()
    mycursor.execute(sql00)
    supplierCurAmnt = mycursor.fetchone()

    sql01 = "insert into PaymentInformation(SupplierId,PaymentDate,Amount,Remark) values('{}','{}','{}','{}')".format(supplierID, txtDateString, varAmount.get(), varRemark.get())
    sql02 = "update suppliersDetails SET supplierCurrAmount = '{}'-'{}' where Id='{}' ".format(supplierCurAmnt[0],varAmount.get(),supplierID)
    mycursor = con.cursor()
    mycursor.execute(sql01)
    mycursor.execute(sql02)
    con.commit()
    messagebox.showinfo("Successful !", "Data has been Added to the Database.", parent=pay)

def Exiting():
    global pay
    x = messagebox.askyesno("Accounting and Inventory", "Do You really want to Exit..?", parent=pay)
    if x == True:
        pay.destroy()

def PaymentDetail(root):
    global pay, comboSupplier, varAmount, varRemark, varAddress, varBalance
    global txtcomboDate, txtcomboMonth, txtcomboYear

    pay = Toplevel(root)

    varAmount = IntVar()
    varRemark = StringVar()
    varAddress = StringVar()
    varBalance = IntVar()

    Label(pay, text="Supplier Name: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=30)
    comboSupplier = ttk.Combobox(pay, width=24)
    comboSupplier.place(x=340, y=30)
    comboSupplier.bind("<<ComboboxSelected>>", GetSupplierDetail)

    LoadSupplierName()

    Label(pay, text="Address: ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=80)
    supplierAdd = Entry(pay, width=27,textvariable = varAddress).place(x=340, y=85)

    Label(pay, text="Balance : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=130)
    txtBalance = Entry(pay, width=27,textvariable = varBalance).place(x=340, y=135)

    Label(pay, text="Payment Date : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=180)
    txtcomboDate = ttk.Combobox(pay, width=4)
    txtcomboDate.place(x=340, y=185)
    txtcomboMonth = ttk.Combobox(pay, width=5)
    txtcomboMonth.place(x=390, y=185)
    txtcomboYear = ttk.Combobox(pay, width=6)
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

    Label(pay, text="Amount : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=230)
    txtAmount = Entry(pay, width=27, textvariable=varAmount).place(x=340, y=235)

    Label(pay, text="Remark : ", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=190, y=280)
    txtRemark = Entry(pay, width=27, textvariable=varRemark).place(x=340, y=285)

    Button(pay, text=" Ok ", width="11", bg="green", fg="white", font=("consolas", 9,"bold"), command=SaveData ).place(x=240, y=350)
    Button(pay, text="Cancel", width="11", bg="red", fg="white", font=("consolas", 9,"bold"), command=Exiting ).place(x=370, y=350)

    pay.title("Payment Screen")
    pay.config(bg="#ffcccc")
    pay.geometry("700x500+300+100")
    pay.mainloop()

#PaymentDetail()