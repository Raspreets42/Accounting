from pythondb import *
from tkinter import *
from tkinter import ttk

def BackScreen():
    itmMaster
    itmMaster.destroy()

def loadItemData():
    global con, tree
    sql = "select * from ItemsDetails"
    mycursor=con.cursor()
    mycursor.execute(sql)
    rsItem=mycursor.fetchall()

    sn=0
    for it in rsItem:
        sn=int(sn)+1
        iId=it[0]
        iName = it[1]
        iQnty = it[2]
        iClQnty = it[3]

        tree.insert("",END,values=[sn,iId,iName,iQnty,iClQnty])

def itemMaster(root):
    global itmMaster, tree
    itmMaster = Toplevel(root)

    Label(itmMaster, text="*  *  *  Stocks Details  *  *  *", bg="#ffcccc",font=("consolas", 12, "bold")).place(x=275, y=20)

    columns = ('c0','c1','c2','c3','c4')
    tree = ttk.Treeview(itmMaster, columns=columns, show='headings')
    tree.heading('c0', text="S.No.")
    tree.heading('c1', text="Item ID")
    tree.heading('c2', text="Item Name")
    tree.heading('c3', text="Item Opening Quantity")
    tree.heading('c4', text="Item Closing Quantity")

    tree.column("c0", width=40)
    tree.column("c1", width=80)
    tree.column("c2", width=150)
    tree.column("c3", width=150)
    tree.column("c4", width=150)

    tree.place(x=135, y=80)

    loadItemData()

    Button(itmMaster, text=" Back ", width="12", bg="red", fg="white", font=("consolas", 12,"bold"),command=BackScreen).place(x=365, y=350)

    itmMaster.title("Stock Details Screen")
    itmMaster.geometry("850x500+250+100")
    itmMaster.config(bg="#ffcccc")

    itmMaster.mainloop()

#itemMaster()