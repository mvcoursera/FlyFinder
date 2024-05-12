from tkinter import *
import tkinter.messagebox
from database import login_provjera
import json
from PIL import Image, ImageTk




# ---------------------------- SAVE PASSWORD ------------------------------- #

def write_json(info_korisnik):
    korisnik = {
        "name": info_korisnik[0],
        "passwd":info_korisnik[1]
    }
    with open("Podaci_login.json", "w") as json_file:
        json.dump(korisnik, json_file, indent=4)

def next_page():
    window.destroy()
    import home_page

def next_signup_page():
    print("---")
    window.destroy()
    import registar

def login_button_provjera():
    print("---")
    password = password_input.get()
    name = user_name_input.get()
    user_name = user_name_input.get()

    taple_info = (name,password)

    if login_provjera(taple_info):
        tkinter.messagebox.showinfo(title="proslo", message=f"Uspjesno ste logovani na {taple_info[0]}")
        write_json(taple_info)
        next_page()
    else:
        tkinter.messagebox.showinfo(title="Pogresan unos", message="Pogresan unos")
        user_name_input.delete(0,END)
        password_input.delete(0,END)

# ----------------------------  UI SETUP ------------------------------- #

window=tkinter.Tk()
window.title("FlyFinder")
window.geometry("600x600")
window.config(bg='#6b98b8')

frame=tkinter.Frame(bg='#6b98b8')

#background img
image = Image.open('./img/slika.jpg')
image = image.resize((600, 300))
image = ImageTk.PhotoImage(image)
image_label = tkinter.Label(window, image=image,bg='#6b98b8')
image_label.pack()

#LOGIN img
login_img = Image.open('./img/login.png')
login_img = login_img.resize((80, 30))
login_img_button=ImageTk.PhotoImage(login_img)

username_label=Label(frame,text="Username:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
password_label= Label(frame,text="Password:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
login_button_label = Button(frame,text="Login",image=login_img_button,fg='#FFFFFF',bg='#6b98b8',borderwidth=0,activebackground='#6b98b8',  command=login_button_provjera)
text_label = Label(frame,text="Don't have an account yet?",font=("Calibri",10,'italic'),fg='#123456',bg='#6b98b8')
signup_button = Button(frame,text="Sign Up here!",font=("Calibri",10,'italic'),fg='#123456',bg='#6b98b8',borderwidth=0,activebackground='#6b98b8',activeforeground='red', command=next_signup_page)

user_name_input=tkinter.Entry(frame,font=("Calibri",12))
password_input=tkinter.Entry(frame,font=("Calibri",12))

username_label.grid(row=0,column=0,pady=5)
password_label.grid(row=1,column=0,pady=5)
login_button_label.grid(row=2,column=1,columnspan=3,pady=20)
user_name_input.grid(row=0,column=1,pady=5)
password_input.grid(row=1,column=1,pady=5)
text_label.grid(row=3,column=1)
signup_button.grid(row=5,column=1)

photo = tkinter.PhotoImage(file = './img/icon4.png')
window.wm_iconphoto(False, photo)

frame.pack()







window.mainloop()

