import streamlit as st
import pandas as pd
from datetime import datetime

# Session state initialization
if 'students' not in st.session_state:
    st.session_state.students = []

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Page config
st.set_page_config(page_title="Student Fee Manager", layout="centered")

# Theme toggle
with st.sidebar:
    st.markdown("## Settings")
    st.session_state.dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)

if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

st.title("🎓 Student Fee Management App")

# Add new student form
with st.expander("➕ Add New Student"):
    with st.form("add_student"):
        name = st.text_input("Student Name")
        contact = st.text_input("Contact Number")
        student_class = st.number_input("Class", min_value=1)
        total_fee = st.number_input("Total Fee", min_value=0)
        first_installment = st.number_input("Initial Paid Fee", min_value=0, max_value=int(total_fee))
        submit = st.form_submit_button("Add Student")

        if submit and name and contact:
            record = {
                "Name": name,
                "Contact": contact,
                "Class": student_class,
                "Total Fee": total_fee,
                "Installments": [first_installment] if first_installment > 0 else [],
                "Paid Fee": first_installment,
                "Pending Fee": total_fee - first_installment,
                "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.students.append(record)
            st.success(f"{name} added successfully!")

# Display and update section
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    st.subheader("💳 Update Installments")
    names = [student["Name"] for student in st.session_state.students]
    selected_name = st.selectbox("Select Student", names)

    selected = next((s for s in st.session_state.students if s["Name"] == selected_name), None)
    if selected:
        new_payment = st.number_input(f"New installment for {selected_name}", min_value=0)
        if st.button("Add Installment"):
            selected["Installments"].append(new_payment)
            selected["Paid Fee"] = sum(selected["Installments"])
            selected["Pending Fee"] = selected["Total Fee"] - selected["Paid Fee"]
            selected["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.success("Installment updated!")

    # Fee summary
    df = pd.DataFrame(st.session_state.students)
    tab1, tab2 = st.tabs(["✅ Completed Fees", "⌛ Pending Fees"])

    with tab1:
        completed = df[df["Pending Fee"] == 0]
        if not completed.empty:
            st.dataframe(completed, use_container_width=True)
        else:
            st.info("No fully paid students.")

    with tab2:
        pending = df[df["Pending Fee"] > 0]
        if not pending.empty:
            st.dataframe(pending, use_container_width=True)
        else:
            st.info("All fees completed!")

    # Full records
    with st.expander("📊 All Student Records"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("No students yet. Add some!")

# Footer
st.markdown("---")
st.markdown("Made with ❤ by Shruti Singh") 