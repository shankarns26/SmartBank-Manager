import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('bank_system.db')
    c = conn.cursor()
    
    # Create accounts table
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (account_number TEXT PRIMARY KEY,
                  name TEXT,
                  balance REAL,
                  created_at TIMESTAMP)''')
    
    # Create transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_account TEXT,
                  to_account TEXT,
                  amount REAL,
                  transaction_type TEXT,
                  timestamp TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Set page config
st.set_page_config(page_title="Bank Management System", layout="wide")

# Main title
st.title("Bank Management System")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Create Account", "View Account", "Transfer Money", "Transaction History"]
)

# Create Account Page
def create_account():
    st.header("Create New Account")
    
    with st.form("create_account_form"):
        name = st.text_input("Full Name")
        initial_deposit = st.number_input("Initial Deposit Amount", min_value=500.0, value=1000.0)
        submit_button = st.form_submit_button("Create Account")
        
        if submit_button and name:
            # Generate unique account number
            account_number = f"ACC{random.randint(10000, 99999)}"
            
            conn = sqlite3.connect('bank_system.db')
            c = conn.cursor()
            
            # Insert new account
            c.execute("INSERT INTO accounts (account_number, name, balance, created_at) VALUES (?, ?, ?, ?)",
                     (account_number, name, initial_deposit, datetime.now()))
            
            # Record initial deposit transaction
            c.execute("""INSERT INTO transactions 
                        (from_account, to_account, amount, transaction_type, timestamp)
                        VALUES (?, ?, ?, ?, ?)""",
                     ('INITIAL', account_number, initial_deposit, 'DEPOSIT', datetime.now()))
            
            conn.commit()
            conn.close()
            
            st.success(f"Account created successfully!\nAccount Number: {account_number}")

# View Account Page
def view_account():
    st.header("View Account Details")
    
    account_number = st.text_input("Enter Account Number")
    if account_number:
        conn = sqlite3.connect('bank_system.db')
        c = conn.cursor()
        
        # Get account details
        c.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
        account = c.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,)).fetchone()
        
        if account:
            st.write("Account Details:")
            st.write(f"Account Holder: {account[1]}")
            st.write(f"Balance: ₹{account[2]:,.2f}")
            st.write(f"Account Created: {account[3]}")
        else:
            st.error("Account not found!")
        
        conn.close()

# Transfer Money Page
def transfer_money():
    st.header("Transfer Money")
    
    with st.form("transfer_form"):
        from_account = st.text_input("From Account Number")
        to_account = st.text_input("To Account Number")
        amount = st.number_input("Amount", min_value=1.0)
        submit_button = st.form_submit_button("Transfer")
        
        if submit_button:
            conn = sqlite3.connect('bank_system.db')
            c = conn.cursor()
            
            # Verify accounts exist
            from_acc = c.execute("SELECT balance FROM accounts WHERE account_number = ?", (from_account,)).fetchone()
            to_acc = c.execute("SELECT balance FROM accounts WHERE account_number = ?", (to_account,)).fetchone()
            
            if from_acc and to_acc:
                if from_acc[0] >= amount:
                    # Update balances
                    c.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, from_account))
                    c.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, to_account))
                    
                    # Record transaction
                    c.execute("""INSERT INTO transactions 
                                (from_account, to_account, amount, transaction_type, timestamp)
                                VALUES (?, ?, ?, ?, ?)""",
                             (from_account, to_account, amount, 'TRANSFER', datetime.now()))
                    
                    conn.commit()
                    st.success("Transfer successful!")
                else:
                    st.error("Insufficient balance!")
            else:
                st.error("One or both accounts not found!")
            
            conn.close()

# Transaction History Page
def transaction_history():
    st.header("Transaction History")
    
    account_number = st.text_input("Enter Account Number")
    if account_number:
        conn = sqlite3.connect('bank_system.db')
        
        # Get all transactions related to the account
        query = """
        SELECT * FROM transactions 
        WHERE from_account = ? OR to_account = ?
        ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(account_number, account_number))
        
        if not df.empty:
            # Format the transactions for display
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.write("Transaction History:")
            st.dataframe(df)
        else:
            st.info("No transactions found for this account.")
        
        conn.close()

# Route to appropriate page based on menu selection
if menu == "Create Account":
    create_account()
elif menu == "View Account":
    view_account()
elif menu == "Transfer Money":
    transfer_money()
elif menu == "Transaction History":
    transaction_history()
