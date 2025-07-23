import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if 'students' not in st.session_state:
    st.session_state.students = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'installments' not in st.session_state:
    st.session_state.installments = {}

# Page config
st.set_page_config(page_title="Student Fee Manager", layout="wide")

# Theme switch
with st.sidebar:
    st.markdown("## Settings")
    st.session_state.dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)

# Apply dark theme manually
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        .css-1aumxhk, .st-bx, .stDataFrame, .stTable {
            background-color: #1c1f26;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("🎓 Student Fee Management App")

# Add Student with Installment First
st.markdown("## 💰 Add Student with Installments")
with st.form("student_form"):
    name = st.text_input("Student Name")
    contact = st.text_input("Contact Number")
    std_class = st.selectbox("Class", list(range(1, 13)))
    installment1 = st.number_input("Installment 1", min_value=0)
    installment2 = st.number_input("Installment 2 (optional)", min_value=0)
    installment3 = st.number_input("Installment 3 (optional)", min_value=0)
    total_fee = st.number_input("Total Fee", min_value=0)
    submit = st.form_submit_button("Save Student")

    if submit and name and contact:
        total_paid = installment1 + installment2 + installment3
        remaining = total_fee - total_paid
        student_id = len(st.session_state.students)
        record = {
            "ID": student_id,
            "Name": name,
            "Contact No": contact,
            "Class": std_class,
            "Total Fee": total_fee,
            "Paid Fee": total_paid,
            "Pending Fee": remaining,
            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.students.append(record)
        st.session_state.installments[student_id] = []
        if installment1:
            st.session_state.installments[student_id].append((datetime.now().strftime("%Y-%m-%d %H:%M"), installment1))
        if installment2:
            st.session_state.installments[student_id].append((datetime.now().strftime("%Y-%m-%d %H:%M"), installment2))
        if installment3:
            st.session_state.installments[student_id].append((datetime.now().strftime("%Y-%m-%d %H:%M"), installment3))
        st.success("Student added successfully!")

# Function to display student table
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    tab1, tab2 = st.tabs(["⌛ Pending Fees", "✅ Completed Fees"])

    with tab1:
        pending_df = df[df["Pending Fee"] > 0].sort_values(by="Pending Fee", ascending=False)
        if not pending_df.empty:
            st.dataframe(pending_df, use_container_width=True)
        else:
            st.info("All fees are completed! Great job!")

    with tab2:
        completed_df = df[df["Pending Fee"] == 0]
        if not completed_df.empty:
            st.dataframe(completed_df, use_container_width=True)
        else:
            st.info("No completed fee records yet.")

    st.markdown("---")
    st.markdown("## ➕ Add New Installment")

    student_names = [f"{s['Name']} (ID: {s['ID']})" for s in st.session_state.students]
    selected_name = st.selectbox("Select Student", student_names)
    selected_id = int(selected_name.split("ID: ")[-1][:-1])
    selected_student = next(s for s in st.session_state.students if s['ID'] == selected_id)

    with st.form("installment_form"):
        new_installment = st.number_input("Installment Amount", min_value=1)
        add_installment = st.form_submit_button("Add Installment")

        if add_installment:
            st.session_state.installments[selected_id].append((datetime.now().strftime("%Y-%m-%d %H:%M"), new_installment))
            total_paid = sum(amount for _, amount in st.session_state.installments[selected_id])
            selected_student['Paid Fee'] = total_paid
            selected_student['Pending Fee'] = selected_student['Total Fee'] - total_paid
            selected_student['Last Updated'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if total_paid <= selected_student['Total Fee']:
                st.success("Installment added successfully!")
            else:
                st.warning("Installments exceed total fee. Consider verifying payment details.")

    st.markdown("## 📜 Installment History")
    for student in st.session_state.students:
        st.subheader(f"{student['Name']} (Class {student['Class']})")
        st.markdown(f"**Total Fee:** ₹{student['Total Fee']} | **Paid:** ₹{student['Paid Fee']} | **Pending:** ₹{student['Pending Fee']}")
        history = st.session_state.installments.get(student['ID'], [])
        if history:
            hist_df = pd.DataFrame(history, columns=["Date", "Amount"])
            st.table(hist_df)
        else:
            st.info("No installments yet.")
else:
    st.info("No student records yet. Add some!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Shruti Singh")
