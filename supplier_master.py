from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    global  suppMaster
    suppMaster.destroy()

def loadSupplierData():
    global con, tree
    sql = "select * from suppliersDetails"
    mycursor=con.cursor()
    mycursor.execute(sql)
    rsSupplier=mycursor.fetchall()

    sn=0
    for itm in rsSupplier:
        sn=int(sn)+1
        sId=itm[0]
        sName = itm[1]
        sAdd = itm[2]
        sMob = itm[3]
        sOpAmount = itm[4]
        sClAmount = itm[5]

        tree.insert("",END,values=[sn,sId,sName,sAdd,sMob,sOpAmount,sClAmount])

def supplierMaster(root):
    global suppMaster, tree
    suppMaster = Toplevel(root)

    Label(suppMaster, text="*  *  *  Suppliers Details  *  *  *", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=340, y=20)

    columns = ('c0','c1','c2','c3','c4','c5','c6')
    tree = ttk.Treeview(suppMaster, columns=columns, show='headings')
    tree.heading('c0', text="S.No.")
    tree.heading('c1', text="Supplier ID")
    tree.heading('c2', text="Supplier Name")
    tree.heading('c3', text="Supplier Address")
    tree.heading('c4', text="Supplier Mobile")
    tree.heading('c5', text="Supplier Opening Amount")
    tree.heading('c6', text="Supplier Closing Amount")

    tree.column("c0", width=40)
    tree.column("c1", width=75)
    tree.column("c2", width=120)
    tree.column("c3", width=120)
    tree.column("c4", width=120)
    tree.column("c5", width=155)
    tree.column("c6", width=155)

    tree.place(x=30, y=80)

    loadSupplierData()

    Button(suppMaster, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=400, y=350)

    suppMaster.title("Supplier Details Screen")
    suppMaster.geometry("1000x500+175+100")
    suppMaster.config(bg="#ffcccc")

    suppMaster.mainloop()


#supplierMaster()