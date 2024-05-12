from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import time
from bs4 import BeautifulSoup
import requests
import json
from selenium.common.exceptions import NoSuchElementException
from my_message import confirm_dialog



# Funkcija koje ce pretraziti let 
def search_fly(send_tuple):
    print(send_tuple)
    FROM_LOCATION = send_tuple[0]
    TO_LOCATION = send_tuple[1]
    BUDGET = send_tuple[2]
    START_DATE = send_tuple[3]
    RETURN_DATE = send_tuple[4]
    print(START_DATE,RETURN_DATE)
    

    print(f"https://www.kayak.ie/flights/{FROM_LOCATION}-{TO_LOCATION}/{START_DATE}/{RETURN_DATE}?sort=price_a")
    # Postavljanje encoding za standardni izlaz na UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options = chrome_options)
    url = f"https://www.kayak.ie/flights/{FROM_LOCATION}-{TO_LOCATION}/{START_DATE}/{RETURN_DATE}?sort=price_a"
    driver.get(url)
    
    time.sleep(10)

    accept_all_xpath = "//button[@class='RxNS RxNS-mod-stretch RxNS-mod-variant-outline RxNS-mod-theme-base RxNS-mod-shape-default RxNS-mod-spacing-base RxNS-mod-size-small']"

    try:
        folder = driver.find_element(By.XPATH, accept_all_xpath)
    except NoSuchElementException:
        print("greska")
        confirm_dialog("Doslo je do greske pri pozivu. Pokusaj ponovo")
        driver.quit()


    # Dobivanje teksta pronađenog elementa


    # Kliknite na pronađeni element
    folder.click()
    time.sleep(5)
    folder2 = driver.find_element(By.XPATH, value='//*[@id="listWrapper"]/div/div[1]/div[1]')
    folder2.click()
    time.sleep(2)
    
    #Uzimamo cijeli karticu(sadrzi sve podatke o letu)
    flight_div_xpath = 'nrc6-inner'
    flight_row = driver.find_elements(By.CLASS_NAME, flight_div_xpath)

    lista_letova = []


    for WebElement in flight_row:
        #elementHTML = WebElement.find_element(By.CLASS_NAME, value = 'f8F1-price-text')

        #temp price je div u kojem se nalaze cijene,broj kofera, klasa voznje
        
        #Uzimamo cijenu lijeta
        price = WebElement.find_element(By.CLASS_NAME, value='f8F1-price-text')
        price_e = price.text
        price_ee = price_e.replace('\u20ac', '')
        price_ee = price_ee.replace(',', '')


        #kofer
        kofer = WebElement.find_elements(By.CLASS_NAME, value='ac27-inner')
        #print(kofer[1].text)

        #broj tasni
        bag = kofer[2].text
        if bag == "":
            bag = "0"

        #klasa leta
        klasa_leta = WebElement.find_element(By.XPATH, value = '//*[@id="listWrapper"]/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div')

        #Link za detalje leta
        link_detalji = WebElement.find_element(By.CSS_SELECTOR, value = '.oVHK a')
        link_sa_detaljima = link_detalji.get_attribute('href')
        
        new_dict = {
            "Price":price_ee,
            "Koferi":kofer[1].text,
            "Torbe":bag,
            "Klasa leta":klasa_leta.text,
            "Link sa detaljima":link_sa_detaljima
        }
        #print(new_dict)
        lista_letova.append(new_dict)
        #Sortiranje niza po keyu Price
        lista_letova.sort(key=lambda x: x["Price"])


    with open("Podaci.json", "w") as json_file:
        json.dump(lista_letova, json_file, indent=4)

    # ---------- SORTIRANJE JSON FILE ----------------
    # Učitaj JSON datoteku
    with open('Podaci.json', 'r') as f: 
        podaci = json.load(f)

    # Sortiraj podatke po određenom ključu
    sortirani_podaci = sorted(podaci, key=lambda x: x['Price'])

    # Napiši sortirane podatke u novu JSON datoteku
    with open('Podaci.json', 'w') as f:
        json.dump(sortirani_podaci, f, indent=4)  # indent=4 za formatiranje

    # Ako je sve proslo kako treba vrati true


def find_fly(budget,bag,kofer):
    with open('Podaci.json', 'r') as file:
        podaci = json.load(file)
    for x in podaci:
        if int(x["Price"]) < float(budget) and int(bag) <= int(x["Torbe"]) and int(kofer) <= int(x["Koferi"]):
            return x
    return False
    




