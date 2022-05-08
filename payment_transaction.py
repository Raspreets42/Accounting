from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    global  payTransaction
    payTransaction.destroy()

def loadPaymentData():
    global con, tree
    sql = "select PaymentID,supplierName,PaymentDate,Amount,Remark from PaymentInformation,suppliersDetails where SupplierId=Id"
    mycursor=con.cursor()
    mycursor.execute(sql)
    rsPayment=mycursor.fetchall()

    for itm in rsPayment:
        pId=itm[0]
        sName = itm[1]
        pDate = itm[2]
        pAmount = itm[3]
        pRemark = itm[4]

        tree.insert("",END,values=[pId,sName,pDate,pAmount,pRemark])

def paymentTransaction(root):
    global payTransaction, tree
    payTransaction = Toplevel(root)

    Label(payTransaction, text="*  *  *  Payments Details  *  *  *", bg="#ffcccc",font=("consolas", 12, "bold")).place(x=265, y=20)

    columns = ('c1','c2','c3','c4','c5')
    tree = ttk.Treeview(payTransaction, columns=columns, show='headings')
    tree.heading('c1', text="Payment ID")
    tree.heading('c2', text="Supplier Name")
    tree.heading('c3', text="Payment Date")
    tree.heading('c4', text="Amount")
    tree.heading('c5', text="Remark")

    tree.column("c1", width=80)
    tree.column("c2", width=130)
    tree.column("c3", width=130)
    tree.column("c4", width=130)
    tree.column("c5", width=130)

    tree.place(x=122, y=80)

    loadPaymentData()

    Button(payTransaction, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=365, y=350)

    payTransaction.title("Payment Details Screen")
    payTransaction.geometry("850x500+250+100")
    payTransaction.config(bg="#ffcccc")

    payTransaction.mainloop()


#paymentTransaction()