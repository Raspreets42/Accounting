from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    global  recptTransaction
    recptTransaction.destroy()

def loadReceiptData():
    global con, tree
    sql = "select ReceiptID,CustomerName,ReceiptDate,Amount,Remark from ReceiptInformation,CustomersDetails where CustomerId=id"
    mycursor=con.cursor()
    mycursor.execute(sql)
    rsReceipt=mycursor.fetchall()

    for itm in rsReceipt:
        rId=itm[0]
        cName = itm[1]
        rDate = itm[2]
        rAmount = itm[3]
        rRemark = itm[4]

        tree.insert("",END,values=[rId,cName,rDate,rAmount,rRemark])

def receiptTransaction(root):
    global recptTransaction, tree
    recptTransaction = Toplevel(root)

    Label(recptTransaction, text="*  *  *  Receipts Details  *  *  *", bg="#ffcccc",font=("consolas", 12, "bold")).place(x=265, y=20)

    columns = ('c1','c2','c3','c4','c5')
    tree = ttk.Treeview(recptTransaction, columns=columns, show='headings')
    tree.heading('c1', text="Receipt ID")
    tree.heading('c2', text="Customer Name")
    tree.heading('c3', text="Receipt Date")
    tree.heading('c4', text="Amount")
    tree.heading('c5', text="Remark")

    tree.column("c1", width=120)
    tree.column("c2", width=120)
    tree.column("c3", width=120)
    tree.column("c4", width=120)
    tree.column("c5", width=120)

    tree.place(x=122, y=80)

    loadReceiptData()

    Button(recptTransaction, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=365, y=350)

    recptTransaction.title("Receipt Details Screen")
    recptTransaction.geometry("850x500+250+100")
    recptTransaction.config(bg="#ffcccc")

    recptTransaction.mainloop()


#receiptTransaction()