from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import json
import mysql.connector
from random import randint,choice,shuffle
from database import write_user_in_base

# ------------------ DATABASE ------------------------





# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def rand_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []


    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    return password



def gen_pass():
    password = rand_pass()
    password_input.delete(0,END)
    password_input.insert(0,password)

# --------------------- INFO CONTROL ----------------------
tld_list = ['.com', '.net', '.org', '.edu', '.gov', 
            '.uk', '.de', '.fr', '.jp', '.cn', 
            '.au', '.ca', '.it', '.nl', '.es', 
            '.us', '.ru', '.ch', '.br', '.se']
def email_control(EMAIL):
    for tld in tld_list:
        if tld in EMAIL and ('@gmail' in EMAIL or 'yahoo' in EMAIL):
            return True
        else:
            return False

def passwd_name_control(passwd,name):
    if len(passwd) > 6 and len(name)> 4:
        return True
    else: 
        return False 
            

# ---------------------------- SAVE INFO ------------------------------- #

def save_pass():
    password = password_input.get()
    email = email_input.get()
    name = user_name_input.get()
    phone_number = phone_number_input.get()

    if email_control(email) and passwd_name_control(password,name):
        taple_info = (name,email,password,phone_number)
        write_user_in_base(taple_info)

        user_name_input.delete(0,END)
        email_input.delete(0,END)
        password_input.delete(0,END)
        phone_number_input.delete(0,END)
    else:
        tkinter.messagebox.showwarning(title="Greska", message="Provjerite da li su sva polja ispunjena i da li je email dobar")





# ---------------------------- UI SETUP ------------------------------- #

window=tkinter.Tk()
window.title("FlyFinder")
window.geometry("600x600")
window.config(bg='#6b98b8')

frame=tkinter.Frame(bg='#6b98b8')

#bckgr img
image = Image.open('./img/slika.jpg')
image = image.resize((600, 300))
image = ImageTk.PhotoImage(image)
image_label = tkinter.Label(window, image=image,bg='#6b98b8')
image_label.pack()
#### submit image
submit_img = Image.open('./img/submit.png')
submit_img = submit_img.resize((80, 30))
submit_img_button=ImageTk.PhotoImage(submit_img)

genpsswd_img = Image.open('./img/btn_gen.png')
genpsswd_img = genpsswd_img.resize((80, 30))
genpswd_img_button=ImageTk.PhotoImage(genpsswd_img)

#-------REGISTER--------------------

register_label=tkinter.Label(frame,text="Register now:",font=("Calibri",15,'italic'),fg='#FFFFFF',bg='#6b98b8')
username_label=tkinter.Label(frame,text="Username:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
email_label=tkinter.Label(frame,text="Email:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
phonenum_label=tkinter.Label(frame,text="Phone number:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))
password_label=tkinter.Label(frame,text="Password:",fg='#123456',bg='#6b98b8',font=("Calibri",10,'italic'))

submit_button_label=tkinter.Button(frame,bg='#6b98b8',fg='#FFFFFF',image=submit_img_button,border=0,activebackground='#6b98b8', command = save_pass)
generate_passwd=tkinter.Button(frame,bg='#6b98b8',fg='#FFFFFF',image=genpswd_img_button,border=0,activebackground='#6b98b8', command = gen_pass)

email_input=tkinter.Entry(frame,font=("Calibri",12))
password_input=tkinter.Entry(frame,font=("Calibri",12))
user_name_input=tkinter.Entry(frame,font=("Calibri",12))
phone_number_input = tkinter.Entry(frame,font=("Calibri",12))


register_label.grid(row=0,column=1, columnspan=2,pady=5)
username_label.grid(row=1,column=0,pady=5)
email_label.grid(row=3,column=0,pady=5)
phonenum_label.grid(row=4,column=0,pady=5)
password_label.grid(row=5,column=0,pady=5)

user_name_input.grid(row=1,column=1,pady=5)
email_input.grid(row=3,column=1,pady=5)
phone_number_input.grid(row=4,column=1,pady=5)
password_input.grid(row=5,column=1,pady=5)

submit_button_label.grid(row=7,column=1,pady=5)
generate_passwd.grid(row=5,column=3,padx=5)

photo = tkinter.PhotoImage(file = './img/icon4.png')
window.wm_iconphoto(False, photo)

frame.pack()

window.mainloop()

