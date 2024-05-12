import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import return_info, find_el, delete_row, add_row, update_row,return_history_info
#from home_page import write_json,read_json
from main import search_fly,find_fly
from my_message import confirm_dialog
from home_page import write_json, read_json

global from_location_input
global to_location_label
global budget_input
global start_date_input
global return_date_input
global kofer_input
global torba_input

global USER_NAME
USER_NAME = home_page.read_json()


def prikazivanje(lista):
    for x in lista:
        status = "Aktivan"
        if x[9] == 0:
            status = "Nektivan"
        tree.insert('', 'end', text="1", values=(status, x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
        print(x)
    info = tree.bind('<<TreeviewSelect>>', listSelected)
    tree.grid(row=0, column=0, columnspan=2)



def listSelected(event):
    selected_rows = tree.selection()
    #print(selected_rows)
    selected_data = []
    for row_id in selected_rows:
        values = tree.item(row_id, 'values')
        selected_data.append(values)


def show():
    from_loc = from_location_input.get()
    to_loc = to_location_input.get()
    budg = budget_input.get()
    start_d = start_date_input.get()
    return_d = return_date_input.get()
    kof = kofer_var.get()
    bag = torba_var.get()
    output = [from_loc, to_loc, budg, start_d, return_d, kof, bag]
    # return output
    return output

window = tk.Tk()

tree = ttk.Treeview(window, column=("id_zahtjeva","userId", "start", "end", "budget", "date_start", "date_end", "kofer", "torba"), show='headings', height=5)

tree.heading("#1", text="Status Zahtjeva")
tree.heading("#2", text="userId")
tree.heading("#3", text="start")
tree.heading("#4", text="end")
tree.heading("#5", text="budget")
tree.heading("#6", text="date_start")
tree.heading("#7", text="date_end")
tree.heading("#8", text="kofer")
tree.heading("#9", text="torba")

lista = return_history_info(USER_NAME)
prikazivanje(lista)

photo = tkinter.PhotoImage(file = './img/icon4.png')
window.wm_iconphoto(False, photo)

window.mainloop()
