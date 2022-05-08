from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    global  purchTransaction
    purchTransaction.destroy()

def loadPurchaseData():
    global con, tree
    sql = "select PurchID,PurchNumber,PurchDate,supplierName,TotalAmount,Remark from PurchaseMain,suppliersDetails where SupplierId=Id"
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

def purchaseTransaction(root):
    global purchTransaction, tree
    purchTransaction = Toplevel(root)

    Label(purchTransaction, text="*  *  *  Purchased Details  *  *  *", bg="#ffcccc", font=("consolas", 12, "bold")).place(x=265, y=20)

    columns = ('c1','c2','c3','c4','c5','c6')
    tree = ttk.Treeview(purchTransaction, columns=columns, show='headings')
    tree.heading('c1', text="Purchase ID")
    tree.heading('c2', text="Purchase Number")
    tree.heading('c3', text="Purchase Date")
    tree.heading('c4', text="Supplier Name")
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

    Button(purchTransaction, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=365, y=350)

    purchTransaction.title("Purchase Details Screen")
    purchTransaction.geometry("850x500+250+100")
    purchTransaction.config(bg="#ffcccc")

    purchTransaction.mainloop()


#purchaseTransaction()