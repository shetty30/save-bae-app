import streamlit as st
import pandas as pd
import datetime

# --- INITIAL SETUP ---
st.set_page_config(page_title="Savebae 💸", layout="centered")
st.title("💖 Savebae — Your Budget Bestie")

# --- BUDGET SETTING ---
st.sidebar.header("💰 Set your Monthly Budget")
budget = st.sidebar.number_input("Enter your budget (₹):", min_value=0)

# --- ADD EXPENSE ---
st.header("🧾 Add an Expense")
with st.form("expense_form"):
    date = st.date_input("Date", datetime.date.today())
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=1)
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add Expense")

# Load or create CSV
try:
    df = pd.read_csv("expenses.csv")
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

# Add new entry
if submitted:
    new_data = pd.DataFrame([[date, category, amount, note]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("expenses.csv", index=False)
    st.success("Bae added your expense 💅")

# --- DISPLAY STATS ---
st.header("📊 Spending Summary")
total_spent = df["Amount"].sum()
remaining = budget - total_spent

col1, col2 = st.columns(2)
col1.metric("Total Spent", f"₹{total_spent}")
col2.metric("Budget Left", f"₹{remaining}")

# Fun nudge
if budget != 0 and remaining < (0.2 * budget):
    st.warning("👀 Bae says: Slow down bestie, budget's crying rn 💸")

# Show expense table
with st.expander("📋 View All Expenses"):
    st.dataframe(df)

