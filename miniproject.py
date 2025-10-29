import sqlite3

# Connect to database (creates file if not exists)
con = sqlite3.connect("bank.db")
cur = con.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS accounts(
    acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    balance REAL
)
''')

def create_account():
    name = input("Enter Full Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    balance = float(input("Enter Initial Deposit: "))
    cur.execute("INSERT INTO accounts(name, age, gender, balance) VALUES (?, ?, ?, ?)", (name, age, gender, balance))
    con.commit()
    print("\n✅ Account created successfully!\n")

def deposit():
    acc = int(input("Enter Account Number: "))
    amount = float(input("Enter Amount to Deposit: "))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no = ?", (amount, acc))
    con.commit()
    print("💰 Amount Deposited Successfully!\n")

def withdraw():
    acc = int(input("Enter Account Number: "))
    amount = float(input("Enter Amount to Withdraw: "))
    cur.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc,))
    data = cur.fetchone()
    if data and data[0] >= amount:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no = ?", (amount, acc))
        con.commit()
        print("💵 Withdrawal Successful!\n")
    else:
        print("⚠️ Insufficient Balance or Invalid Account!\n")

def check_balance():
    acc = int(input("Enter Account Number: "))
    cur.execute("SELECT name, balance FROM accounts WHERE acc_no = ?", (acc,))
    data = cur.fetchone()
    if data:
        print(f"👤 Account Holder: {data[0]} | 💰 Balance: ₹{data[1]:.2f}\n")
    else:
        print("❌ Account not found!\n")

def display_accounts():
    cur.execute("SELECT * FROM accounts")
    for row in cur.fetchall():
        print(row)
    print()

def delete_account():
    acc = int(input("Enter Account Number to Delete: "))
    cur.execute("DELETE FROM accounts WHERE acc_no = ?", (acc,))
    con.commit()
    print("🗑️ Account Deleted Successfully!\n")

# Main Menu
while True:
    print("""
========= 🏦 BANK MANAGEMENT SYSTEM =========
1. Create New Account
2. Deposit Money
3. Withdraw Money
4. Check Balance
5. Display All Accounts
6. Delete Account
7. Exit
============================================
""")

    choice = input("Enter your choice: ")

    if choice == '1':
        create_account()
    elif choice == '2':
        deposit()
    elif choice == '3':
        withdraw()
    elif choice == '4':
        check_balance()
    elif choice == '5':
        display_accounts()
    elif choice == '6':
        delete_account()
    elif choice == '7':
        print("Thank you for using our system! 🙏")
        break
    else:
        print("⚠️ Invalid Choice! Please try again.\n")

con.close()
