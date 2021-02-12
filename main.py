from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import password_generator
import encryption


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def fill_password():
    global window2, nr_letters_entry, nr_symbols_entry, nr_numbers_entry

    nr_letters = nr_letters_entry.get()
    nr_symbols = nr_symbols_entry.get()
    nr_numbers = nr_numbers_entry.get()

    if len(nr_letters) == 0 or len(nr_symbols) == 0 or len(nr_numbers) == 0:
        messagebox.showerror(title="Empty Fields", message="Please make sure you haven't left any fields empty")
        return

    if nr_letters.isdigit() != 1 or nr_symbols.isdigit() != 1 or nr_numbers.isdigit() != 1:
        messagebox.showerror(title="Not Digits", message="Please make sure you entered only digits in the fields")
        return

    generated_password = password_generator.generate_password(int(nr_letters), int(nr_symbols), int(nr_numbers))

    pyperclip.copy(generated_password)  # Copying the password to the clipboard

    password_entry.delete(0, 'end')
    password_entry.insert(END, generated_password)
    window2.destroy()


def generate():
    global window2, nr_letters_entry, nr_symbols_entry, nr_numbers_entry
    window2 = Toplevel(window)
    window2.title("Generate Password")
    window2.config(padx=50, pady=50)
    window2.resizable(False, False)
    window2.attributes('-topmost', 1)

    letters_label = Label(window2, text="How many LETTERS would you like in your password?")
    letters_label.grid(column=0, row=0)
    nr_letters_entry = Entry(window2)
    nr_letters_entry.focus()
    nr_letters_entry.grid(column=1, row=0, padx=(5, 5), pady=(10, 10))

    symbols_label = Label(window2, text="How many SYMBOLS would you like in your password?")
    symbols_label.grid(column=0, row=1)
    nr_symbols_entry = Entry(window2)
    nr_symbols_entry.grid(column=1, row=1, padx=(5, 5), pady=(10, 10))

    numbers_label = Label(window2, text="How many NUMBERS would you like in your password?")
    numbers_label.grid(column=0, row=2)
    nr_numbers_entry = Entry(window2)
    nr_numbers_entry.grid(column=1, row=2, padx=(5, 5), pady=(10, 10))

    done_button = Button(window2, text="Generate", command=fill_password)
    done_button.grid(column=0, row=3, padx=(5, 5), pady=(10, 10))

    window2.mainloop()


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_details():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": encryption.encrypt_message(password)
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Empty Fields", message="Please make sure you haven't left any fields empty")
        return
    # messagebox.showinfo(title="Title", message="This is a message")
    is_ok = messagebox.askokcancel(title=f"Confirm details for {website}", message=f"Details entered: "
                                                                                   f"\n\nEmail : {email}\n"
                                                                                   f"Password : {password} "
                                                                                   f"\n\nIs it ok to save?")

    if is_ok:
        try:  # When the file is not present or is empty
            with open("data.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = new_data
        else:
            data.update(new_data)
        finally:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

    website_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            email = data[website]["email"]
            password = encryption.decrypt_message(data[website]["password"])
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror(title="Error", message="No data found.")
    except KeyError:
        messagebox.showerror(title="Error", message=f"No details, for the website {website}, exist.")
    else:
        messagebox.showinfo(title=website, message=f"Email : {email}\nPassword : {password}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(False, False)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website :")
website_label.grid(column=0, row=1, pady=(10, 10))

email_label = Label(text="Email/Username :")
email_label.grid(column=0, row=2, pady=(10, 10))

password_label = Label(text="Password :")
password_label.grid(column=0, row=3, pady=(10, 10))

# Entries
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="NEWS", padx=(5, 5), pady=(10, 10))
website_entry.focus()

email_entry = Entry()
email_entry.grid(column=1, row=2, columnspan=2, sticky="NEWS", padx=(5, 5), pady=(10, 10))
email_entry.insert(0, "your_email@gmail.com")

password_entry = Entry(show="*")
password_entry.grid(column=1, row=3, sticky="NEWS", padx=(5, 5), pady=(10, 10))

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW", padx=(5, 5), pady=(10, 10))

generate_pass = Button(text="Generate Password", command=generate)
generate_pass.grid(column=2, row=3, sticky="EW", padx=(5, 5), pady=(10, 10))

add_button = Button(text="Add", command=add_details)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW", padx=(5, 5), pady=(10, 10))

window.mainloop()
