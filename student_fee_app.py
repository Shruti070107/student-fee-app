
import streamlit as st
import pandas as pd
import os

# CSV file path
DATA_FILE = "students.csv"

# Initialize CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Name", "Contact", "Total Fee", "Paid Fee", "Pending Fee"])
    df_init.to_csv(DATA_FILE, index=False)

# Load data
df = pd.read_csv(DATA_FILE)

# Title and watermark
st.markdown("""
    <h1 style='text-align: center; color: white;'>🎓 Student Fee Manager</h1>
    <p style='text-align: center; color: gray;'>Made by Shruti Singh</p>
    <hr style='border: 1px solid gray;'>
""", unsafe_allow_html=True)

# Add new student
st.subheader("➕ Add Student")
with st.form("add_form"):
    name = st.text_input("Student Name")
    contact = st.text_input("Contact Number")
    total_fee = st.number_input("Total Fee", min_value=0)
    paid_fee = st.number_input("Paid Fee", min_value=0)
    submitted = st.form_submit_button("Add Student")

    if submitted:
        pending_fee = total_fee - paid_fee
        new_data = pd.DataFrame([[name, contact, total_fee, paid_fee, pending_fee]],
                                columns=["Name", "Contact", "Total Fee", "Paid Fee", "Pending Fee"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Student added successfully!")
        st.experimental_rerun()

# Search by name
st.subheader("🔍 Search Student")
search_name = st.text_input("Enter name to search")
if search_name:
    filtered_df = df[df['Name'].str.contains(search_name, case=False)]
    st.dataframe(filtered_df, use_container_width=True)

# Delete student
st.subheader("❌ Delete Student")
delete_contact = st.text_input("Enter contact number to delete")
if st.button("Delete"):
    if delete_contact in df["Contact"].values:
        df = df[df["Contact"] != delete_contact]
        df.to_csv(DATA_FILE, index=False)
        st.success("Student deleted successfully!")
        st.experimental_rerun()
    else:
        st.error("Contact not found!")

# Separate pending and completed data
pending_df = df[df["Pending Fee"] > 0]
completed_df = df[df["Pending Fee"] == 0]

# Style functions
def style_pending(df):
    return df.style.set_properties(**{
        'background-color': '#660000',  # dark red
        'color': 'white',
        'border-color': 'white'
    })

def style_completed(df):
    return df.style.set_properties(**{
        'background-color': '#003300',  # dark green
        'color': 'white',
        'border-color': 'white'
    })

# Two-column layout
st.subheader("📊 Fee Summary")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 Students with Pending Fees")
    if not pending_df.empty:
        st.dataframe(style_pending(pending_df), use_container_width=True)
    else:
        st.success("No pending fees!")

with col2:
    st.markdown("### 🟢 Students with Completed Fees")
    if not completed_df.empty:
        st.dataframe(style_completed(completed_df), use_container_width=True)
    else:
        st.warning("No fees completed yet.")