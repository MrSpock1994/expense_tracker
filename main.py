import sqlite3
from tkinter import *
from tkinter import ttk
import pandas as pd

root = Tk()
root.title("Personal Expenses")
root.geometry("245x130")
style = ttk.Style(root)


def new_expense():
    global expense_name
    global expense_price
    global expense_date
    global expense_description
    global new_expense_window 
    new_expense_window = Toplevel()
    new_expense_window.title("New Expense")
    new_expense_window.geometry("240x220")
    expense_name = ttk.Entry(new_expense_window, width=25)
    expense_name.insert(END, "Name")
    expense_name.grid(row=0, column=0, padx=6, pady=3)
    expense_price = ttk.Entry(new_expense_window, width=25)
    expense_price.grid(row=1, column=0, padx=6, pady=3)
    expense_price.insert(END, "Price")
    expense_date = ttk.Entry(new_expense_window, width=25)
    expense_date.insert(END, "Date")
    expense_date.grid(row=2, column=0, padx=6, pady=3)
    expense_description = Text(new_expense_window, height=4, width=25)
    expense_description.insert(END, "Description")
    expense_description.grid(row=3, column=0, padx=6, pady=3)
    button_confirm_new_expense = ttk.Button(new_expense_window, text="Add expense", command=confirm_new_expense)
    button_confirm_new_expense.grid(row=4, column=0, padx=6, pady=3)


def confirm_new_expense():
    conn = sqlite3.connect("Expenses.db")
    cursor = conn.cursor()
    insert_expense = [expense_name.get(), expense_price.get(), expense_date.get(), expense_description.get("1.0", 'end')]
    cursor.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)", insert_expense)
    expense_name.delete(0, END)
    expense_price.delete(0, END)
    expense_date.delete(0, END)
    expense_description.delete(1.0, END)
    expense_name.insert(END, "Name")
    expense_price.insert(END, "Price")
    expense_date.insert(END, "Date")
    expense_description.insert(END, "Description")
    conn.commit()
    conn.close()
    sucessfull_add= ttk.Label(new_expense_window, text="Expense add sucessfully!")
    sucessfull_add.grid(row=5, column=0, padx=6, pady=3)


def delete_expense():
    global expense_delete
    global delete_expense_window 
    delete_expense_window = Toplevel()
    delete_expense_window.title("Delete Expense")
    delete_expense_window.geometry("220x120")
    expense_delete= ttk.Entry(delete_expense_window, width=25)
    expense_delete.insert(END, "Insert here the ID to delete")
    expense_delete.grid(row=0, column=0, padx=6, pady=3)
    button_confirm_delete_expense = ttk.Button(delete_expense_window, text="Delete expense", command=confirm_delete_expense)
    button_confirm_delete_expense.grid(row=1, column=0, padx=6, pady=3)


def confirm_delete_expense():
    conn = sqlite3.connect("Expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE oid = " + expense_delete.get())
    conn.commit()
    conn.close()
    sucessfull_deleted = ttk.Label(delete_expense_window, text=f"ID {expense_delete.get()} deleted!")
    sucessfull_deleted.grid(row=2, column=0, padx=6, pady=3)
    expense_delete.delete(0, END)



def export_all():
    conn = sqlite3.connect("Expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT *, oid  FROM expenses")
    records = cursor.fetchall()
    name = []
    price = []
    date = []
    description = []
    id = []
    for c in range(0, len(records)):
        name.append(records[c][0])
        price.append(records[c][1])
        date.append(records[c][2])
        description.append(records[c][3].rstrip())
        id.append(records[c][4])
    mydf = pd.DataFrame(list(zip(name, price, date, description, id)),columns = ["Name", "Price", "Date", "Description", "ID"])
    file_name = 'Expenses.xlsx'
    mydf.to_excel(file_name, index=False, header=True)

button_new_expanse = ttk.Button(root, text="New Expense", command=new_expense)
button_new_expanse.grid(row=1, column=0, ipadx=74, pady=5)

button_export_all = ttk.Button(root, text="Export all", command=export_all)
button_export_all.grid(row=2, column=0, ipadx=82, pady=5)

button_delete_expense = ttk.Button(root, text="Delete Expense", command=delete_expense)
button_delete_expense.grid(row=3, column=0, ipadx=68, pady=5)
root.mainloop()