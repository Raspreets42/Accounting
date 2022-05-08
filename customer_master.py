from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    global  custoMaster
    custoMaster.destroy()

def loadCustomerData():
    global con, tree
    sql = "select * from CustomersDetails"
    mycursor=con.cursor()
    mycursor.execute(sql)
    rsCustomer=mycursor.fetchall()

    sn=0
    for itm in rsCustomer:
        sn=int(sn)+1
        cId=itm[0]
        cName = itm[1]
        cAdd = itm[2]
        cMob = itm[3]
        cOpAmount = itm[4]
        cClAmount = itm[5]

        tree.insert("",END,values=[sn,cId,cName,cAdd,cMob,cOpAmount,cClAmount])

def customerMaster(root):
    global custoMaster, tree
    custoMaster = Toplevel(root)

    Label(custoMaster, text="*  *  *  Customers Details  *  *  *", bg="#ffcccc", font=("consolas", 12,"bold")).place(x=340,y=20)

    columns = ('c0','c1','c2','c3','c4','c5','c6')
    tree = ttk.Treeview(custoMaster, columns=columns, show='headings')
    tree.heading('c0', text="S.No.")
    tree.heading('c1', text="Customer ID")
    tree.heading('c2', text="Customer Name")
    tree.heading('c3', text="Customer Address")
    tree.heading('c4', text="Customer Mobile")
    tree.heading('c5', text="Customer Opening Amount")
    tree.heading('c6', text="Customer Closing Amount")

    tree.column("c0", width=40)
    tree.column("c1", width=80)
    tree.column("c2", width=110)
    tree.column("c3", width=110)
    tree.column("c4", width=110)
    tree.column("c5", width=155)
    tree.column("c6", width=155)

    tree.place(x=30, y=80)

    loadCustomerData()

    Button(custoMaster, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=400, y=350)

    custoMaster.title("Customer Details Screen")
    custoMaster.geometry("900x500+175+100")
    custoMaster.config(bg="#ffcccc")

    custoMaster.mainloop()


#customerMaster()