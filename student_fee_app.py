import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json

# Load existing data or initialize
if os.path.exists("students.json"):
    with open("students.json", "r") as f:
        students = json.load(f)
else:
    students = []

# Theme Toggle
theme_mode = st.sidebar.radio("Theme Mode", ["Light", "Dark"])
if theme_mode == "Dark":
    st.markdown(
        """
        <style>
            body {
                background-color: #111;
                color: white;
            }
            .stApp {
                background-color: #1e1e1e;
                color: white;
            }
            div[data-testid="stSidebar"] {
                background-color: #222;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            body {
                background-color: #f5f5f5;
                color: black;
            }
            .stApp {
                background-color: #ffffff;
                color: black;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Watermark (Enhanced)
st.markdown("""
<div style='position: fixed; bottom: 10px; right: 10px; opacity: 0.7; font-size: 14px; font-family: Arial; color: #888;'>
    🚀 Made with ❤️ by <strong>Shruti Singh</strong>
</div>
""", unsafe_allow_html=True)

st.title("📚 Student Fee Management System")

menu = ["Add Student", "View Students", "Search by Name"]
choice = st.sidebar.selectbox("Menu", menu)

# Helper function to save students list
def save_students():
    with open("students.json", "w") as f:
        json.dump(students, f)

if choice == "Add Student":
    st.subheader("➕ Add Student")
    name = st.text_input("Name")
    contact = st.text_input("Contact Number")
    student_class = st.selectbox("Class", list(range(1, 13)))
    installment1 = st.number_input("Installment 1", min_value=0, value=0, step=100)
    installment2 = st.number_input("Installment 2", min_value=0, value=0, step=100)
    installment3 = st.number_input("Installment 3 (Optional)", min_value=0, value=0, step=100)

    if st.button("Add"):
        total_paid = installment1 + installment2 + installment3
        total_fee = 50000  # Example total fee
        pending_fee = total_fee - total_paid

        students.append({
            "name": name,
            "contact": contact,
            "class": student_class,
            "installments": [installment1, installment2, installment3],
            "total_paid": total_paid,
            "total_fee": total_fee,
            "pending_fee": pending_fee
        })
        save_students()
        st.success("Student added successfully!")

elif choice == "View Students":
    st.subheader("📖 All Students")
    if students:
        df = pd.DataFrame(students)
        df['installment1'] = df['installments'].apply(lambda x: x[0])
        df['installment2'] = df['installments'].apply(lambda x: x[1])
        df['installment3'] = df['installments'].apply(lambda x: x[2])

        selected_student = st.selectbox("Select student to delete", [s['name'] for s in students])
        del_btn = st.button("❌ Delete Selected", key="del")
        if del_btn:
            students[:] = [s for s in students if s['name'] != selected_student]
            save_students()
            st.success("Deleted successfully")
            st.experimental_rerun()

        st.dataframe(df[['name', 'contact', 'class', 'installment1', 'installment2', 'installment3', 'total_paid', 'total_fee', 'pending_fee']])

        total_pending = df['pending_fee'].sum()
        total_completed = df['total_paid'].sum()
        st.markdown(f"""<h4 style='color: green;'>✅ Total Completed Fees: ₹{total_completed}</h4>""", unsafe_allow_html=True)
        st.markdown(f"""<h4 style='color: red;'>🔴 Total Pending Fees: ₹{total_pending}</h4>""", unsafe_allow_html=True)

        st.markdown("---")
        chart = px.bar(df, x='name', y='pending_fee', title='Pending Fees Chart', color='pending_fee', color_continuous_scale='reds')
        st.plotly_chart(chart)
    else:
        st.info("No students added yet.")

elif choice == "Search by Name":
    st.subheader("🔍 Search Student")
    search_name = st.text_input("Enter Name")
    if search_name:
        result = [s for s in students if search_name.lower() in s['name'].lower()]
        if result:
            df = pd.DataFrame(result)
            df['installment1'] = df['installments'].apply(lambda x: x[0])
            df['installment2'] = df['installments'].apply(lambda x: x[1])
            df['installment3'] = df['installments'].apply(lambda x: x[2])
            st.dataframe(df[['name', 'contact', 'class', 'installment1', 'installment2', 'installment3', 'total_paid', 'total_fee', 'pending_fee']])
        else:
            st.warning("No student found.")
