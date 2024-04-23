from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import bcrypt
import sqlite3
from tkinter import messagebox



def close_open():
    window.destroy()
    fulecheck()



def virsi():

    url = 'https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas'
    fule_type= ['dd', '95e', '98e', 'lpg' ]

    x=0
    x1=1
    for i in fule_type:
        fule_type_bs4= fule_type[x]
        x+=1
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            price_card_div = soup.find('div', {'class': 'price-card', 'data-type': fule_type_bs4})

            if price_card_div:
                span_elements = price_card_div.find_all('span')

                if len(span_elements) > 1:
                    number_text = span_elements[1].text.strip()

                    try:
                        number = float(number_text)
                        virsi_insert = f"{fule_type_bs4}: {number} EUR"
                        global listbox_neste, listbox_virsi
                        listbox_virsi.insert(x1, virsi_insert)
                        x1 += 1
                    except ValueError:
                        print("Unable to convert the text to a number:", number_text)
            else:
                print("Div element with class 'price-card' and data-type '95e' not found on the page.")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)



def neste():
    url = 'https://www.neste.lv/lv/content/degvielas-cenas'
    response = requests.get(url)

    fule_type = [ '95e', '98e', 'dd', 'dd-pro']

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        fuel_info_div = soup.find('div', {'class': 'field__item even', 'property': 'content:encoded'})

        if fuel_info_div:
            tr_elements = fuel_info_div.find_all('tr')
            x=0
            x1=1

            for tr_element in tr_elements:
                span_elements = tr_element.find_all('span')

                if len(span_elements) > 1:
                    number_text = span_elements[1].text.strip()

                    try:
                        number = float(number_text)
                        neste_insert = f"{fule_type[x]}: {number} EUR"

                        global listbox_neste, listbox_virsi
                        
                        listbox_neste.insert(x1, neste_insert)
                        x1 += 1
                        x += 1
                    except ValueError:
                        print("Unable to convert the text to a number:", number_text)
        else:
            print("Div element with class 'field__item even' and property 'content:encoded' not found on the page.")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)



def circle_k():
    url = 'https://www.circlek.lv/uznemumiem/b2b-degvielas-cenas'
    response = requests.get(url)

    fule_type = ['95e', '98e', 'dd', 'dd-Plus','lpg']

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        fuel_info_div = soup.find('div', class_='ck-prices-per-product')

        if fuel_info_div:
            tr_elements = fuel_info_div.find_all('tr')

            x = 0
            x1 = 1
            for tr_element in tr_elements:
                
                div_elements = tr_element.find_all('div')

                if len(div_elements) > 2:
                    number_text = div_elements[2].text.strip()

                    parts = number_text.split(':')
                    if len(parts) > 1:
                        number_part = parts[1].strip()
                        try:
                            number = float(number_part.replace(',', '.'))
                            circle_k_insert = f"{fule_type[x]}: {number} EUR"
                            x1 += 1
                            x += 1

                            global listbox_circle_k
                            listbox_circle_k.insert(x1, circle_k_insert)
                            
                        except ValueError:
                            print("Unable to convert the text to a number:", number_part)
                    else:
                        print("Number not found in text:", number_text)
        else:
            print("Div element with class 'ck-prices-per-product' not found on the page.")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)



def viad():
    url = 'https://www.viada.lv/zemakas-degvielas-cenas/'
    response = requests.get(url)

    fule_type = ['95e', '95e+', '98e', 'dd', 'dd-multi', 'lpg', 'e85']
    x = 0
    x1 = 1


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        fuel_info_div = soup.find('div', class_='the_content_wrapper')

        if fuel_info_div:
            tr_elements = fuel_info_div.find_all('tr')

            for i, tr_element in enumerate(tr_elements, start=1):
                td_elements = tr_element.find_all('td')

                if len(td_elements) > 1:
                    number_text = td_elements[1].text.strip()

                    match = re.search(r'([\d.,]+)', number_text)
                    if match:
                        number_part = match.group(1)
                        number_part = number_part.replace(',', '.')
                        try:
                            number = float(number_part)
                            viad_insert = f"{fule_type[x]}: {number} EUR"
                            x1 += 1
                            x += 1

                            global listbox_viad
                            listbox_viad.insert(x, viad_insert)

                        except ValueError:
                            print("Unable to convert the text to a number:", number_part)
                    else:
                        print("Number not found in text:", number_text)
        else:
            print("Div element with class 'the_content_wrapper' not found on the page.")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)



def fulecheck():
    window_2 = tk.Tk()
    window_2.title('Fuelchecker')
    window_2.geometry('740x440')
    window_2.configure(bg="#747880")
    frame = tk.Frame(window_2, width=600, height=400, relief=tk.RIDGE, bd=2)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    global listbox_neste, listbox_virsi, listbox_circle_k, listbox_viad

    heading = tk.Label(frame, text='DEGVILAS CENAS!')
    heading.grid(column=0, row=1, sticky=tk.W, padx=20, pady=1)

    station1 = tk.Label(frame, text='VIRŠI')
    station1.grid(column=0, row=2, sticky=tk.W, padx=20, pady=1)

    listbox_virsi = Listbox(frame, height = 7, width = 25)
    listbox_virsi.grid(column=0, row=3, sticky=W, pady=1, padx=10)

    station2 = tk.Label(frame, text='NESTE')
    station2.grid(column=2, row=2, sticky=tk.W, padx=20, pady=1)

    listbox_neste = Listbox(frame, height = 7, width = 25)
    listbox_neste.grid(column=2, row=3, sticky=W, pady=1, padx=10)

    station3 = tk.Label(frame, text='CIRCLE K')
    station3.grid(column=3, row=2, sticky=tk.W, padx=20, pady=1)

    listbox_circle_k = Listbox(frame, height = 7, width = 25)
    listbox_circle_k.grid(column=3, row=3, sticky=W, pady=1, padx=10)

    station3 = tk.Label(frame, text='VIAD')
    station3.grid(column=4, row=2, sticky=tk.W, padx=20, pady=1)

    listbox_viad = Listbox(frame, height = 7, width = 25)
    listbox_viad.grid(column=4, row=3, sticky=W, pady=1, padx=10)
    
    
    virsi(), neste(), circle_k(), viad()

    window_2.mainloop()



def signup():
    username = login_entry2.get()
    password = password_entry2.get()
    if username != '' and password != '':
        cursor.execute('SELECT username FROM users WHERE username = ?', [username])
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Username already exists')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute('INSERT INTO users VALUES (?, ?)', [username, hashed_password])
            connection.commit()
            messagebox.showinfo('Success', 'Account has been created!')
    else:
        messagebox.showerror('Error', 'Enter all data!')



def login_acc():
    username = login_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username = ?', [username])
        result = cursor.fetchone()
        if result:
            hashed_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password): 
                messagebox.showinfo('Success', 'Logged successfully!')
                close_open()
            else:
                messagebox.showerror('Error', 'Invalid password!')
        else:
            messagebox.showerror('Error', 'Invalid username!')
    else:
        messagebox.showerror('Error', 'Enter all data!')



def login_window():
    frame1.destroy()

    global login_entry2, password_entry2, frame2

    frame2 = tk.Frame(window, width=300, height=200, relief=tk.RIDGE, bd=2)
    frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    welcome = tk.Label(frame2, text='Reģistrē jaunu kontu!')
    welcome.grid(column=0, row=0, sticky=tk.W, padx=20, pady=1)

    login_name = tk.Label(frame2, text='Lietotājvārds')
    login_name.grid(column=0, row=1, sticky=tk.W, padx=20, pady=1)

    login_entry2 = tk.Entry(frame2, width=40)
    login_entry2.grid(column=0, row=2, sticky=tk.W, padx=20, pady=1)

    password_name = tk.Label(frame2, text='Parole')
    password_name.grid(column=0, row=3, sticky=tk.W, padx=20, pady=1)

    password_entry2 = tk.Entry(frame2, width=40, show='*')
    password_entry2.grid(column=0, row=4, sticky=tk.W, padx=20, pady=1)

    login_button = tk.Button(frame2, text="Reģistrēties", bg="#fc766a", fg="white", width=34, height=2, command=signup, cursor="hand2")
    login_button.grid(column=0, row=5, sticky=tk.W, padx=20, pady=10)

    signup_button = tk.Button(frame2, text="Ielogojies", bg=frame2.cget("background"), fg="#fc766a", relief=tk.FLAT, command=close_open2, underline=-1, cursor="hand2")
    signup_button.grid(column=0, row=6, sticky=tk.W, padx=20, pady=20)



def close_open2():
    window.destroy()
    startapp()



def startapp():
    global login_entry, password_entry, frame1, window, cursor, connection
    

    window = tk.Tk()
    window.title("Log in")
    window.geometry("400x300")
    window.configure(bg="#747880")

    frame1 = tk.Frame(window, width=300, height=200, relief=tk.RIDGE, bd=2)
    frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    connection = sqlite3.connect('login_data.db')
    cursor = connection.cursor()

    command = """CREATE TABLE IF NOT EXISTS users
        (username TEXT NOT NULL, 
        password TEXT NOT NULL)"""
    cursor.execute(command)
    connection.commit()


    welcome = tk.Label(frame1, text='Sveiks!')
    welcome.grid(column=0, row=0, sticky=tk.W, padx=20, pady=1)

    login_name = tk.Label(frame1, text='Lietotājvārds')
    login_name.grid(column=0, row=1, sticky=tk.W, padx=20, pady=1)

    login_entry = tk.Entry(frame1, width=40)
    login_entry.grid(column=0, row=2, sticky=tk.W, padx=20, pady=1)

    password_name = tk.Label(frame1, text='Parole')
    password_name.grid(column=0, row=3, sticky=tk.W, padx=20, pady=1)

    password_entry = tk.Entry(frame1, width=40, show='*')  # Use show='*' to display asterisks
    password_entry.grid(column=0, row=4, sticky=tk.W, padx=20, pady=1)

    login_button = tk.Button(frame1, text="Pieslēgties", bg="#fc766a", fg="white", width=34, height=2, command=login_acc, cursor="hand2")
    login_button.grid(column=0, row=5, sticky=tk.W, padx=20, pady=10)

    signup_button = tk.Button(frame1, text="Nav konta?", bg=frame1.cget("background"), fg="#fc766a", relief=tk.FLAT, command=login_window, underline=-1, cursor="hand2")
    signup_button.grid(column=0, row=6, sticky=tk.W, padx=20, pady=20)


    window.mainloop()



startapp()
