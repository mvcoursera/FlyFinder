import mysql.connector
from tkinter import *
import tkinter.messagebox

# ------------------ DATABASE ------------------------
db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Kikiriki9989.',
    database = 'flyfinder'
)


def write_user_in_base(tuple_info):
    mycursor = db.cursor()
    #KREIRANJE TABELE Person sa kolonama(ID,NAME,EMAIL,PASSWD,PHONE_NUMBER)
    #mycursor.execute("CREATE TABLE Person(ID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), email VARCHAR(50), passwd VARCHAR(50), phone VARCHAR(50))")

    Q2 = f"SELECT * FROM Person WHERE name = '{tuple_info[0]}'"
    mycursor.execute(Q2)
    result_name = mycursor.fetchone()
    
    if result_name is None:
    #Ubacivanje novog korisnika u bazu
        Q1 = "INSERT INTO Person(name,email,passwd,phone) VALUES(%s,%s,%s,%s)"
        mycursor.execute(Q1, tuple_info)
        db.commit()
        tkinter.messagebox.askokcancel(title = "website",  message = "Uspjesno se registrovani")
        
        mycursor.execute("SELECT * FROM Person")
        for x in mycursor:
            print(x)
    else:
        tkinter.messagebox.showwarning("Warning","Korisnik sa ovim User vec postoji")


def login_provjera(tuple_info):
    mycursor = db.cursor()
    Q1 = f"SELECT * FROM Person WHERE name = %s AND passwd = %s"
    mycursor.execute(Q1,tuple_info)
    result = mycursor.fetchone()

    if result is None: 
        return False
    else:
        return True


#Trazimo neki element iz tabele Person kokretno za id i email
def find_el(el,user_name):
    mycursor = db.cursor()
    Q1 = f"SELECT {el} FROM Person WHERE name = %s"
    parametri = (user_name,)

    mycursor.execute(Q1, parametri)
    rezultat = mycursor.fetchone()
    return rezultat[0]


# mycursor = db.cursor()
# Q1 = """CREATE TABLE Fly_Request
#          (id_zahtjeva int PRIMARY KEY AUTO_INCREMENT,
#          userId int,
#          start VARCHAR(10),
#          end VARCHAR(10),
#          budget FLOAT,
#          date_start DATE,
#          date_end DATE,
#          kofer BOOLEAN,
#          torba BOOLEAN
#          )"""
# mycursor.execute(Q1)

def add_request(info_tuple):
    mycursor = db.cursor()
    Q1 = """INSERT INTO fly_request(userId,start,end,budget,date_start,date_end,kofer,torba) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
    mycursor.execute(Q1,info_tuple)
    db.commit()


#Funkcija koja trazi sve requestove sa odredjenim ID koprinika

def request_search(USER_ID):
    mycursor = db.cursor()
    Q1 = "SELECT * FROM fly_request WHERE userId = %s"
    mycursor.execute(Q1,(USER_ID,))
    row = mycursor.fetchall()
    return row

# ---------------- Upiti za request page ----------------------

def return_info(user_name):
    mycursor = db.cursor()
    Q1 = "SELECT * FROM fly_request WHERE userId = %s AND status = 1"
    USER_ID = find_el("ID",user_name)
    mycursor.execute(Q1,(USER_ID,))
    return_list = mycursor.fetchall()
    return return_list

def return_history_info(user_name):
    mycursor = db.cursor()
    Q1 = "SELECT * FROM fly_request WHERE userId = %s"
    USER_ID = find_el("ID",user_name)
    mycursor.execute(Q1,(USER_ID,))
    return_list = mycursor.fetchall()
    return return_list

def delete_row(user_id):
    mycursor = db.cursor()
    Q1 = "UPDATE fly_request SET status = 0 WHERE id_zahtjeva = %s" #Samo mjenjamo colonu statu
    mycursor.execute(Q1,(user_id,))
    db.commit()
    print(user_id)

def add_row(info_tuple):
    mycursor = db.cursor()
    Q1 = "INSERT INTO fly_request(userId,start,end,budget,date_start,date_end,kofer,torba) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(Q1,info_tuple)
    db.commit()


def update_row(info_tuple):
    mycursor = db.cursor()
    Q1 = "UPDATE fly_request SET start = %s, end = %s, budget = %s, date_start = %s, date_end = %s, kofer = %s, torba = %s WHERE id_zahtjeva = %s"
    mycursor.execute(Q1, info_tuple)  # Promenjen način prosleđivanja parametara
    db.commit()




