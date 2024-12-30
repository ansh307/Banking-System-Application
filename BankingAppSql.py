import mysql.connector as my
from datetime import datetime
import random
import re

def create_database():
    con = my.connect(host="localhost", user="root", password="1234")
    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS banking_system")
    con.close()

    con = my.connect(host="localhost", user="root", password="1234", database="banking_system")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        account_number VARCHAR(10) UNIQUE NOT NULL,
        dob DATE NOT NULL,
        city VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        balance FLOAT NOT NULL,
        contact_number VARCHAR(10) NOT NULL,
        email_id VARCHAR(255) NOT NULL,
        address TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_number VARCHAR(10) NOT NULL,
        type VARCHAR(50) NOT NULL,
        amount FLOAT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES users (account_number)
    )''')

    con.commit()
    con.close()

def generate_account_number():
    return ''.join(random.choices('0123456789', k=10))

def validate_email(email):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, email)

def validate_contact_number(contact):
    return len(contact) == 10 and contact.isdigit()

def validate_password(password):
    return len(password) >= 8 and any(char.isupper() for char in password) and any(char.isdigit() for char in password)

def add_user():
    con = my.connect(host="localhost", user="root", password="1234", database="banking_system")
    cur = con.cursor()

    name = input("Enter name: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    city = input("Enter city: ")
    password = input("Enter password: ")
    while not validate_password(password):
        print("Password must be at least 8 characters long, contain an uppercase letter, and a digit.")
        password = input("Enter password: ")
    balance = float(input("Enter initial balance (minimum 2000): "))
    while balance < 2000:
        print("Initial balance must be at least 2000.")
        balance = float(input("Enter initial balance: "))
    contact_number = input("Enter contact number: ")
    while not validate_contact_number(contact_number):
        print("Invalid contact number. Must be 10 digits.")
        contact_number = input("Enter contact number: ")
    email_id = input("Enter email ID: ")
    while not validate_email(email_id):
        print("Invalid email format.")
        email_id = input("Enter email ID: ")
    address = input("Enter address: ")

    account_number = generate_account_number()
    print(f"Generated account number: {account_number}")

    cur.execute('''INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email_id, address) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (name, account_number, dob, city, password, balance, contact_number, email_id, address))

    con.commit()
    con.close()
    print("User added successfully.")

def show_users():
    con = my.connect(host="localhost", user="root", password="1234", database="banking_system" )
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    for user in users:
        print("\nUser Information:")
        print(f"ID: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"Account Number: {user[2]}")
        print(f"DOB: {user[3]}")
        print(f"City: {user[4]}")
        print(f"Balance: {user[6]}")
        print(f"Contact: {user[7]}")
        print(f"Email: {user[8]}")
        print(f"Address: {user[9]}")
        print(f"Active: {'Yes' if user[10] else 'No'}")

    con.close()

def login():
    con = my.connect(host="localhost", user="root", password="1234", database="banking_system")
    cur = con.cursor()

    account_number = input("Enter account number: ")
    password = input("Enter password: ")

    cur.execute("SELECT * FROM users WHERE account_number = %s AND password = %s", (account_number, password))
    user = cur.fetchone()

    if user:
        print("Login successful.")
        while True:
            print("\n1. Show Balance")
            print("2. Credit Amount")
            print("3. Debit Amount")
            print("4. Transfer Amount")
            print("5. Change Password")
            print("6. Update Profile")
            print("7. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                print(f"Your current balance is: {user[6]}")

            elif choice == '2':
                amount = float(input("Enter amount to credit: "))
                user[6] += amount
                cur.execute("UPDATE users SET balance = %s WHERE account_number = %s", (user[6], account_number))
                cur.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'Credit', %s)", (account_number, amount))

            elif choice == '3':
                amount = float(input("Enter amount to debit: "))
                if amount > user[6]:
                    print("Insufficient balance.")
                else:
                    user[6] -= amount
                    cur.execute("UPDATE users SET balance = %s WHERE account_number = %s", (user[6], account_number))
                    cur.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'Debit', %s)", (account_number, amount))

            elif choice == '4':
                target_account = input("Enter target account number: ")
                amount = float(input("Enter amount to transfer: "))

                if amount > user[6]:
                    print("Insufficient balance.")
                else:
                    cur.execute("SELECT * FROM users WHERE account_number = %s", (target_account,))
                    target_user = cur.fetchone()

                    if target_user:
                        user[6] -= amount
                        target_user[6] += amount
                        cur.execute("UPDATE users SET balance = %s WHERE account_number = %s", (user[6], account_number))
                        cur.execute("UPDATE users SET balance = %s WHERE account_number = %s", (target_user[6], target_account))

                        cur.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'Transfer Out', %s)", (account_number, amount))
                        cur.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'Transfer In', %s)", (target_account, amount))
                        print("Transfer successful.")
                    else:
                        print("Target account not found.")

            elif choice == '5':
                new_password = input("Enter new password: ")
                while not validate_password(new_password):
                    print("Password must be at least 8 characters long, contain an uppercase letter, and a digit.")
                    new_password = input("Enter new password: ")

                cur.execute("UPDATE users SET password = %s WHERE account_number = %s", (new_password, account_number))
                print("Password updated successfully.")

            elif choice == '6':
                name = input("Enter new name: ")
                city = input("Enter new city: ")
                email_id = input("Enter new email ID: ")
                while not validate_email(email_id):
                    print("Invalid email format.")
                    email_id = input("Enter new email ID: ")
                address = input("Enter new address: ")

                cur.execute("UPDATE users SET name = %s, city = %s, email_id = %s, address = %s WHERE account_number = %s",
                            (name, city, email_id, address, account_number))
                print("Profile updated successfully.")

            elif choice == '7':
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please try again.")

            con.commit()

    else:
        print("Invalid login credentials.")

    con.close()

def main():
    create_database()

    while True:
        print("\nBANKING SYSTEM")
        print("1. Add User")
        print("2. Show Users")
        print("3. Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            show_users()
        elif choice == '3':
            login()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
