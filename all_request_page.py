import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import return_info, find_el, delete_row, add_row, update_row
from home_page import write_json,read_json
from main import search_fly,find_fly
from my_message import confirm_dialog
from datetime import datetime

global from_location_input
global to_location_label
global budget_input
global start_date_input
global return_date_input
global kofer_input
global torba_input

global USER_NAME
USER_NAME = read_json()

def provjera_datuma(datum,id_zahtjeva):
    # Dobijanje današnjeg datuma
    print(datum)
    danas = datetime.now().date()
    if datum < danas:
        print("-*----")
        delete_row(id_zahtjeva)

def go_back():
    window.destroy()
    import login

def go_to_history():
    window.destroy()
    import history_request

def delete_all_items(tree):
    items = tree.get_children()
    for item in items:
        tree.delete(item)


def prikazivanje(lista):
    for x in lista:
        tree.insert('', 'end', text="1", values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
        provjera_datuma(x[5],x[0])
    info = tree.bind('<<TreeviewSelect>>', listSelected)
    tree.grid(row=0, column=0, columnspan=2)

def delete_selected_row():
    response = confirm_dialog('Da li ste sigurni da zelite da izbrisete')
    if response:
        selected_item_id = listSelected(None)
        delete_row(selected_item_id)
        delete_all_items(tree)
        prikazivanje(return_info(USER_NAME))


def update_selected_row():
    response = confirm_dialog("Da li zelite pretragu leta pod novim uslovima")
    if response:
        send_list = show()
        id_zahtjeva = listSelected(None)
        send_list.append(id_zahtjeva)
        clear_input()
        update_row(send_list)
        delete_all_items(tree)
        prikazivanje(return_info(USER_NAME))
        info_fly = send_list[:-1]
        print(info_fly)
        print(send_list)
        sreach_fly(send_list)
        fly = find_fly(info_fly[2],info_fly[5],info_fly[6])
        print(fly)
        if fly:
            print("nasli smo")
            delete_row(id_zahtjeva)
            delete_all_items(tree)
            prikazivanje(return_info(USER_NAME))
        else:
            messagebox.showinfo(title="Nije pronadjen let", message="Let pod ovim uslovima nije pronadjen sacekajte")




def listSelected(event):
    selected_rows = tree.selection()
    #print(selected_rows)
    selected_data = []
    for row_id in selected_rows:
        values = tree.item(row_id, 'values')
        selected_data.append(values)

    clear_input()

    if selected_data:
        from_location_input.insert(0, selected_data[0][2])
        to_location_input.insert(0, selected_data[0][3])
        budget_input.insert(0, selected_data[0][4])
        start_date_input.insert(0, selected_data[0][5])
        return_date_input.insert(0, selected_data[0][6])
        kofer_var.set(selected_data[0][7])
        torba_var.set(selected_data[0][8])

    if selected_data:
        selected_item_id = selected_data[0][0]
        return selected_item_id

def clear_input():
    from_location_input.delete(0, tk.END)
    to_location_input.delete(0, tk.END)
    budget_input.delete(0, tk.END)
    start_date_input.delete(0, tk.END)
    return_date_input.delete(0, tk.END)
    kofer_var.set(0)
    torba_var.set(0)

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

tree = ttk.Treeview(window, column=("id_zahtjev", "userId", "start", "end", "budget", "date_start", "date_end", "kofer", "torba"), show='headings', height=5)

tree.heading("#1", text="id_zahtjev")
tree.heading("#2", text="userId")
tree.heading("#3", text="start")
tree.heading("#4", text="end")
tree.heading("#5", text="budget")
tree.heading("#6", text="date_start")
tree.heading("#7", text="date_end")
tree.heading("#8", text="kofer")
tree.heading("#9", text="torba")

lista = return_info(USER_NAME)
prikazivanje(lista)

from_location_label = ttk.Label(text="From:")
to_location_label = ttk.Label(text="To:")
budget_label = ttk.Label(text="Budget:")
start_date = ttk.Label(text="Start:")
return_date = ttk.Label(text="Return:")
kofer = ttk.Label(text="Kofer:")
torba = ttk.Label(text="Torba:")

from_location_input = ttk.Entry()
to_location_input = ttk.Entry()
budget_input = ttk.Entry()
start_date_input = ttk.Entry()
return_date_input = ttk.Entry()


# Promena unosnih polja u check boxove
kofer_var = tk.IntVar()
torba_var = tk.IntVar()
kofer_input = ttk.Checkbutton(window, text="Kofer", variable=kofer_var)
torba_input = ttk.Checkbutton(window, text="Torba", variable=torba_var)

from_location_label.grid(row=1, column=0)
to_location_label.grid(row=2, column=3)
budget_label.grid(row=3, column=0)
start_date.grid(row=4, column=0)
return_date.grid(row=5, column=0)
kofer.grid(row=6, column=0)
torba.grid(row=7, column=0)

from_location_input.grid(row=1, column=1)
to_location_input.grid(row=2, column=1)
budget_input.grid(row=3, column=1)
start_date_input.grid(row=4, column=1)
return_date_input.grid(row=5, column=1)
kofer_input.grid(row=6, column=1)
torba_input.grid(row=7, column=1)

delete_btn = ttk.Button(text="delete", command=delete_selected_row)
clear_btn = ttk.Button(text="Clear", command=clear_input)
update_btn = ttk.Button(text="Update", command=update_selected_row)
return_back_btn = ttk.Button(text="Back", command=go_back)

delete_btn.grid(row=9, column=0, columnspan=2)
clear_btn.grid(row=8, column=1)
update_btn.grid(row=10, column=0, columnspan=2)
return_back_btn.grid(row=11, column=0)

photo = tkinter.PhotoImage(file = './img/icon4.png')
window.wm_iconphoto(False, photo)

window.mainloop()
