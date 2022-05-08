from pythondb import *
from supplier import *
from customer import *
from item import *
from purchese import *
from sales import *
from payment import *
from receipt import *
from customer_master import *
from supplier_master import *
from purchase_transaction import *
from sales_transaction import *
from payment_transaction import *
from receipt_transaction import *
from item_master import *
from tkinter import *
from PIL import ImageTk  #pip install pillow <- command prompt

def menubar(top):
    global root
    root = Toplevel(top)
    root.title("Menu Screen")

    bg = ImageTk.PhotoImage(file="menubarimg.jpeg")
    labelI = Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    menubar = Menu(root)
    masterfile = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Master", menu=masterfile)
    masterfile.add_command(label="Supplier", command=lambda: supplierDetail(root))
    masterfile.add_command(label="Customer", command=lambda: customerDetail(root))
    masterfile.add_command(label="Item", command=lambda: ItemDetail(root))

    transactionfile = Menu(menubar, tearoff=0)
    transactionfile.add_command(label="Purchase", command=lambda: PurcheseDetail(root))
    transactionfile.add_command(label="Sales", command=lambda: SalesDetail(root))
    transactionfile.add_command(label="Payment", command=lambda: PaymentDetail(root))
    transactionfile.add_command(label="Receipt", command=lambda: ReceiptDetail(root))

    menubar.add_cascade(label="Transaction", menu=transactionfile)

    reportsfile = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Reports", menu=reportsfile)

    rptMaster = Menu(reportsfile, tearoff=0)
    reportsfile.add_cascade(label="Master Report", menu=rptMaster)

    rptMaster.add_command(label="Supplier Data", command=lambda: supplierMaster(root))
    rptMaster.add_command(label="Customer Data", command=lambda: customerMaster(root))

    rptTransaction = Menu(reportsfile, tearoff=0)
    reportsfile.add_cascade(label="New Transaction", menu=rptTransaction)
    rptTransaction.add_command(label="Purchase Data", command=lambda: purchaseTransaction(root))
    rptTransaction.add_command(label="Sales Data", command=lambda: salesTransaction(root))
    rptTransaction.add_command(label="Payment Data", command=lambda: paymentTransaction(root))
    rptTransaction.add_command(label="Receipt Data", command=lambda: receiptTransaction(root))

    reportsfile.add_command(label="Stock Data", command=lambda: itemMaster(root))

    root.config(menu=menubar)

    root.geometry("700x500+300+100")
    root.mainloop()

#menubar()
