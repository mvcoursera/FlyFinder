from datetime import datetime
from tkinter import *
import tkinter
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox, ttk
from tkcalendar import *
from main import search_fly
import json
from main import find_fly
from twilio.rest import Client
from database import find_el,add_request
import smtplib
from find_fly_request import find_request,search_request_fly
from datetime import datetime



my_mail = "finderfly22@gmail.com"
my_passwd = "atje abeh xdvj rdjp"

account_sid = "AC85b330157114465542df41e5771d2431"
auth_token = "01e5e5d9f041fc87679fe44fa124d9e3"



# Nakon što je user_name postavljen u login.py, možete ga koristiti u home_page.py
def read_json():
    with open('Podaci_login.json', 'r') as file:
        podaci = json.load(file)
    user_name = podaci['name']
    with open('Podaci_login.json', 'w') as file:
        json.dump({}, file)
    return user_name

def write_json(info_korisnik):
    korisnik = {
        "name": info_korisnik[0],
        "passwd":info_korisnik[1]
    }
    with open("Podaci_login.json", "w") as json_file:
        json.dump(korisnik, json_file, indent=4)

# ----------------------- Uzimamo aerodrome i json fila -----------------------------
with open("airports.json") as file:
    podaci = json.load(file)


only_airport = [element for element in podaci if element["type"] == "airport"]
list_of_city = []
list_of_city_skr = []
for name in only_airport:
    if name["name"] != None:
        list_of_city.append(name["name"])
        list_of_city_skr.append(name["iata"])

def air_location(from_loc,to_loc):
    print(from_loc,to_loc)
    if from_loc != to_loc:
        from_loc_indx = list_of_city.index(from_loc)
        from_loc_skraceno = list_of_city_skr[from_loc_indx]

        to_loc_index = list_of_city.index(to_loc)
        to_loc_skraceno = list_of_city_skr[to_loc_index]
        print(f"airport -> {from_loc_skraceno} -> {to_loc_skraceno}")
        print(type(from_loc_skraceno))
        air_tuple = (from_loc_skraceno,to_loc_skraceno)
        return air_tuple
    else:
        return False


# ---------------------------------------------------------------------

# ------------------ Funkcija koja provjerava regularnost datuma --------------
def provjera_datuma(start_datum_str, return_datum_str):
    danas = datetime.now().date()
    start_datum = datetime.strptime(start_datum_str, "%Y-%m-%d").date()
    return_datum = datetime.strptime(return_datum_str, "%Y-%m-%d").date()

    if (start_datum < return_datum) and (start_datum > danas):
        return True
    else:
        print(f"{start_datum} -> {return_datum} -> {danas}")
        return False

# ----------------------------------------------------------------------

def go_request():
    send_tup = (USER_NAME,"---")
    write_json(send_tup)
    window.destroy()
    import all_request_page

def go_to_history():
    send_tup = (USER_NAME,"---")
    write_json(send_tup)
    window.destroy()
    import history_request

def send_info():
    from_loc = from_combobox.get()
    to_loc = to_combobox.get()
    airport_skraceno = air_location(from_loc,to_loc)

    bag = var10.get()
    kofer = var20.get()
    budget = price_entry.get()

    start_date = cal_departure.get()
    end_date = cal_return.get()
    validation_date = provjera_datuma(start_date,end_date)
    print(validation_date)
    if airport_skraceno and validation_date and budget:
        from_loc = airport_skraceno[0]
        to_loc = airport_skraceno[1]
        #info_tuple = (user_id,from_loc,to_loc,budget,start_date,end_date,bag,kofer)
        info_tuple = (from_loc, to_loc, budget, start_date, end_date, bag, kofer)
        print(info_tuple)
        return info_tuple
    else:
        tkinter.messagebox.showerror(title="Greska u sezonu", message="Provjerite da li imate prazno polje ili gresku u datumu",)
        return False


def send_button_fun():
    info_tuple = send_info()
    if info_tuple:
        print(info_tuple)
        search_fly(info_tuple)
        budget = info_tuple[2]
        bag = info_tuple[5]
        kofer = info_tuple[6]
        fly = find_fly(budget,bag,kofer)
        if fly != False:
            print(fly)
            price = fly["Price"]
            link = fly["Link sa detaljima"]
            koferi = fly["Koferi"]
            torbe = fly["Torbe"]

            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body = f'Cijena je: {price}, link je: {link}, broj kofera: {koferi}, broj torbi(Rucni prtljag): {torbe}',
                from_='+13134837435',
                to='+38267085709'
            )
            email = find_el("email",USER_NAME)
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_mail, password=my_passwd)
                connection.sendmail(from_addr=my_mail,
                            to_addrs=email,
                            msg = f"Subject:Pronadjen Let!!!\n\n Cijena je: {price}, link je: {link}, broj kofera: {koferi}, broj torbi(Rucni prtljag): {torbe}")

        #Ako nije zahtjev smjestamo u bazu(fly_request)
        else:
            print("nismo nasli")
            user_id = find_el("ID", USER_NAME)
            # print(user_id)
            # print(info_tuple)
            send_tuple = (user_id,info_tuple[0],info_tuple[1],info_tuple[2],info_tuple[3],info_tuple[4],info_tuple[5],info_tuple[6])
            add_request(send_tuple)
            #TODO: Dati neku poruku korisniku
            tkinter.messagebox.showinfo(title="Nije pronadjen let", message="Let pod ovim uslovima nije pronadjen sacekajte")


# --------------------- Funkcije za update list boxa -------------------
def update_listbox(data, listbox):
    listbox.delete(0, END)
    for item in data:
        listbox.insert(END, item)

def fillout(event, entry, listbox):
    entry.delete(0, END)
    entry.insert(0, listbox.get(ACTIVE))

def check(e, entry, listbox):
    typed = entry.get()
    if typed == '':
        data = list_of_city
    else:
        data = [item for item in list_of_city if typed.lower() in item.lower()]
    update_listbox(data, listbox)
# -----------------------------------------------------------------------
# ----Uzimanjen user_namea ulogavanog korisnika
global USER_NAME
USER_NAME = read_json()
passws = "---"


# ---------------------- GUI -------------------------
print(USER_NAME)

window = tkinter.Tk()
window.title("FlyFinder")
window.geometry("800x800")  
window.config(bg='#6b98b8')

photo = tkinter.PhotoImage(file ='img/icon4.png')
window.wm_iconphoto(False, photo)

frame=tkinter.Frame(window,bg='#6b98b8')


var10=IntVar()
var20=IntVar()

check_10kg=Checkbutton(frame, text="10kg",variable=var10)
check_10kg.deselect()
check_20kg=Checkbutton(frame, text="20 kg",variable=var20)
check_20kg.deselect()

#-------REGISTER--------------------
options=["Option 1", "Option 2", "Option 3", "Option 4"]

from_label = tkinter.Label(frame,text="From:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'),justify=CENTER)
from_label.grid(row=0, column=0, padx=10, pady=10)
# from_combox = ttk.Combobox(frame, values=list_of_city)
# to_combobox = ttk.Combobox(frame, values=list_of_city)

from_combobox = tkinter.Entry(frame,width=30)
from_combobox.grid(row=0, column=1, padx=10, pady=10)
my_list = Listbox(frame,width=30)
my_list.grid(row=1, column=1,padx=10)

update_listbox(list_of_city, my_list)
my_list.bind("<<ListboxSelect>>", lambda event: fillout(event, from_combobox, my_list))
from_combobox.bind("<KeyRelease>", lambda e: check(e, from_combobox, my_list))


to_label = Label(frame,text="To:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'),justify=CENTER)
to_label.grid(row=0, column=2)
to_combobox = Entry(frame,width=30)
to_combobox.grid(row=0, column=3)
my_list2 = Listbox(frame,width=30)
my_list2.grid(row=1, column=3,padx=10)

update_listbox(list_of_city, my_list2)
my_list2.bind("<<ListboxSelect>>", lambda event: fillout(event, to_combobox, my_list2))
to_combobox.bind("<KeyRelease>", lambda e: check(e, to_combobox, my_list2))

day_departure_label=tkinter.Label(frame,text="Day of departure:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'),justify=CENTER)
day_departure_label.grid(row=2,column=0,pady=10,padx=10)
cal_departure = DateEntry(frame, date_pattern="yyyy-mm-dd",width=25)
cal_departure.grid(row=2,column=1,pady=10,padx=10)

day_return_label=tkinter.Label(frame,text="Day of return:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'),justify=CENTER)
day_return_label.grid(row=2,column=2,pady=10,padx=10)
cal_return = DateEntry(frame, date_pattern="yyyy-mm-dd",width=25)
cal_return.grid(row=2,column=3,pady=10,padx=10)

luggage_label=tkinter.Label(frame,text="Choose luggage:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
luggage_label.grid(row=3,column=0, padx=10, pady=10)
check_10kg.grid(row=3,column=1, padx=0, pady=10)
check_20kg.grid(row=4,column=1,pady=0,padx=10)

num_passengers_label=tkinter.Label(frame,text="Buget:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
num_passengers_label.grid(row=5,column=0, padx=10, pady=10)
price_entry = tkinter.Entry(frame)
price_entry.grid(row=5,column=1, padx=10, pady=10)


request_button_label = tkinter.Button(frame,text="Submit",bg='#274051',fg='#FFFFFF',font=("Calibri",12,'italic'),border=0,command = send_button_fun,width=20)
request_button_label.grid(row=6,column=1,pady=20,padx=20)

all_request_btn = tkinter.Button(frame,text="View request",bg='#274051',fg='#FFFFFF',font=("Calibri",12,'italic'),border=0,command = go_request,width=20)
all_request_btn.grid(row=6,column=2,pady=20,padx=20)

view_history = tkinter.Button(frame,text="View History",bg='#274051',fg='#FFFFFF',font=("Calibri",12,'italic'),border=0,command = go_to_history,width=20)
view_history.grid(row=6,column=3,pady=20,padx=20)


frame.pack()


window.mainloop()