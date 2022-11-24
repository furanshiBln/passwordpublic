from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------------------ #
HEADING_WIDTH = 15
HEADING_FONT = ["Arial", 12, "bold"]
ENTRY_FONT = ["Arial", 10]
COLOR = "white"
BORDER = "grey"
RED = "#f2f3f4"
SPACE = 3
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8,10))]
    password_symbols = [choice(symbols) for _ in range(randint(2,4))]
    password_numbers = [choice(numbers) for _ in range(randint(2,4))]

    password_generated = password_numbers + password_symbols + password_letters
    shuffle(password_generated)

    password = "".join(password_generated)
    password_entry.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_entry():
    website = website_entry.get()
    password = password_entry.get()
    username = username_entry.get()

    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showerror(title="Whoopsie!", message="Looks like you left a field blank. \nPlease make "
                                                        "sure there "
                                                        "is an entry for each field!.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open ("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            password_entry.delete(0, END)
            username_entry.delete(0, END)
            website_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            username = data[website]["email"]
            username_entry.insert(0,username)
            password = data[website]["password"]
            password_entry.insert(0, password)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")
# ---------------------------- UI SETUP ------------------------------- #

#Setup Window + Picture
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=COLOR)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(10,10,image=logo_img, anchor="nw")
canvas.config(bg=COLOR, highlightthickness=0)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website: ", font=HEADING_FONT, anchor="e", width=HEADING_WIDTH, bg=COLOR, padx=SPACE,pady=SPACE)
website_label.config(fg="black")
website_label.grid(row=1,column=0)

username_label = Label(text="Email/Username: ", font=HEADING_FONT, anchor="e", width=HEADING_WIDTH, bg=COLOR,padx=SPACE,pady=SPACE)
username_label.config(fg="black")
username_label.grid(row=2,column=0)

password_label = Label(text="Password: ", font=HEADING_FONT, anchor="e", width=HEADING_WIDTH, bg=COLOR,padx=SPACE,pady=SPACE)
password_label.config(fg="black")
password_label.grid(row=3,column=0)

pseudo_label = Label(text="Pseudo: ", font=HEADING_FONT, anchor="e", width=HEADING_WIDTH, padx=SPACE,pady=SPACE)
password_label.grid(row=3,column=0)

#Entries
website_entry = Entry(width=35)
website_entry.config(highlightthickness=1, highlightbackground=BORDER, font=ENTRY_FONT)
website_entry.grid(row=1, column=1, columnspan=2)

username_entry = Entry(width=60)
username_entry.insert(END, string="")
username_entry.config(highlightthickness=1, highlightbackground=BORDER,font=ENTRY_FONT)
username_entry.grid(row=2, column=1,columnspan=3)

password_entry = Entry(width=35)
password_entry.insert(END, string="")
password_entry.config(highlightthickness=1, highlightbackground=BORDER, font=ENTRY_FONT)
password_entry.grid(row=3,column=1, columnspan=2)

#Buttons
generate_pw_button = Button(text=" generate password ", command=generate_password, font=HEADING_FONT)
generate_pw_button.config(bg=RED, highlightbackground=BORDER, highlightthickness=1, width=16)
generate_pw_button.grid(row=3,column=3, pady=2, padx=5)

add_entry = Button(text=" save entry ", command=save_entry, font=HEADING_FONT)
add_entry.config(bg=RED, highlightbackground=BORDER, highlightthickness=1)
add_entry.grid(row=4, column=1,pady=10, padx=10)

search_entry = Button(text=" search ", command=find_password, font=HEADING_FONT)
search_entry.config(bg=RED, highlightbackground=BORDER, highlightthickness=1, width=16)
search_entry.grid(row=1, column=3,pady=2, padx=5)


window.mainloop()
