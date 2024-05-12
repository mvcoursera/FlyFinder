import json
from main import search_fly,find_fly
from database import find_el,request_search
from twilio.rest import Client
import smtplib

# --------------------- SEND EMAIL AND SMS ------------------



def send_mail_sms(PRICE,LINK,EMAIL):
    my_mail = "finderfly22@gmail.com"
    my_passwd = "atje abeh xdvj rdjp"

    account_sid = "AC85b330157114465542df41e5771d2431"
    auth_token = "01e5e5d9f041fc87679fe44fa124d9e3"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body = f'Provjeri mail, pronasli smo let',
            from_='+13134837435',
            to='+38267085709'
    )
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_mail, password=my_passwd)
        connection.sendmail(from_addr=my_mail, 
            to_addrs=EMAIL, 
            msg = f"Subject:Pronadjen Let!!!\n\n {PRICE} , {LINK}")


# ------------------------- Funkcija koja iz tabele fly_request projevara sve zahtjeve REGISTROVANOG korisnika
def find_request(user_name):
    id_user = find_el("ID", user_name)
    print(id_user)
    #Niz sa svim letovi korisnika 
    info_tuple = request_search(id_user)
    #print(request_search(id_user))
    for info_fly in info_tuple:
        request_id = info_fly[0]
        from_location = info_fly[2]
        to_location = info_fly[3]
        budget = info_fly[4]
        start_date = info_fly[5]
        end_date = info_fly[6]
        end_tuple = (from_location,to_location,budget,start_date,end_date)
        search_fly(end_tuple)

        # Ako je let pronadjen saljem mail i brisemo ga iz baze, ako ne nista 
        if find_fly(budget) != False:
            fly = find_fly(budget)
            price = fly["Price"]
            link = fly["Link sa detaljima"]
            email = find_el("email",user_name)

            send_mail_sms(price,link,email)
            #!!!! delete_request(request_id)

            # print("Nasli smo")
            # print(request_id)
        else:
            print("Nismo nasli")

def search_request_fly(user_name):
    id_user = find_el("ID", user_name)
    #Niz sa svim letovi korisnika 
    info_tuple = request_search(id_user)
    if info_tuple == []:
        print("Nema requestova")
    else:
        for info_fly in info_tuple:
            request_id = info_fly[0]
            from_location = info_fly[2]
            to_location = info_fly[3]
            budget = info_fly[4]
            start_date = info_fly[5]
            end_date = info_fly[6]
            print(request_id,from_location,to_location)


        


    
