from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    global  salTransaction
    salTransaction.destroy()

def loadPurchaseData():
    global con, tree
    sql = "select SaleID,SaleNumber,SalesDate,CustomerName,TotalAmount,Remark from SalesMain,CustomersDetails where CustomerId=id"
    mycursor=con.cursor()
    mycursor.execute(sql)
    rsPurchase=mycursor.fetchall()

    for itm in rsPurchase:
        pId=itm[0]
        pNumber = itm[1]
        pDate = itm[2]
        sName=itm[3]
        pAmount = itm[4]
        pRemark = itm[5]

        tree.insert("",END,values=[pId,pNumber,pDate,sName,pAmount,pRemark])

def salesTransaction(root):
    global salTransaction, tree
    salTransaction = Toplevel(root)

    Label(salTransaction, text="*  *  *  Sales Details  *  *  *", bg="#ffcccc",font=("consolas", 12, "bold")).place(x=280, y=20)

    columns = ('c1','c2','c3','c4','c5','c6')
    tree = ttk.Treeview(salTransaction, columns=columns, show='headings')
    tree.heading('c1', text="Sales ID")
    tree.heading('c2', text="Sales Number")
    tree.heading('c3', text="Sales Date")
    tree.heading('c4', text="Customer Name")
    tree.heading('c5', text="Total Amount")
    tree.heading('c6', text="Remark")

    tree.column("c1", width=80)
    tree.column("c2", width=120)
    tree.column("c3", width=135)
    tree.column("c4", width=135)
    tree.column("c5", width=120)
    tree.column("c6", width=120)

    tree.place(x=65, y=80)

    loadPurchaseData()

    Button(salTransaction, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=365, y=350)

    salTransaction.title("Sales Details Screen")
    salTransaction.geometry("850x500+250+100")
    salTransaction.config(bg="#ffcccc")

    salTransaction.mainloop()


#salesTransaction()