import tkinter as tk

# -------------- Alert za potvrdu ----------------
def confirm_dialog(message):
    confirm = tk.Toplevel()
    confirm.title("Potvrda")
    label = tk.Label(confirm, text=message)
    label.pack(padx=20, pady=20)

    def confirm_true():
        confirm.user_response = True
        confirm.destroy()

    def confirm_false():
        confirm.user_response = False
        confirm.destroy()

    confirm.user_response = None

    confirm_button = tk.Button(confirm, text="Potvrdi", command=confirm_true)
    confirm_button.pack(side=tk.LEFT, padx=10)
    cancel_button = tk.Button(confirm, text="Otkaži", command=confirm_false)
    cancel_button.pack(side=tk.RIGHT, padx=10)
    
    photo = tkinter.PhotoImage(file = './img/icon4.png')
    confirm.wm_iconphoto(False, photo)

    confirm.wait_window(confirm)

    return confirm.user_response
#----------------------------------------------

