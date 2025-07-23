import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state if not already done
if 'students' not in st.session_state:
    st.session_state.students = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Page config
st.set_page_config(page_title="Student Fee Manager", layout="centered")

# Theme switch
with st.sidebar:
    st.markdown("## Settings")
    st.session_state.dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)

# Apply dark theme manually (Streamlit Cloud themes are limited)
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("🎓 Student Fee Management App")

# Form to add/edit students
with st.expander("➕ Add New Student"):
    with st.form("student_form"):
        name = st.text_input("Student Name")
        contact= st.text_input("Contact Number")
        class= st.text_input("Class")
        total_fee = st.number_input("Total Fee", min_value=0)
        paid_fee = st.number_input("Paid Fee", min_value=0, max_value=int(total_fee))
        submit = st.form_submit_button("Save Student")

        if submit and name and contact:
            remaining = total_fee - paid_fee
            record = {
                "Name": name,
                "Contact No": contact,
                "Class": class,
                "Total Fee": total_fee,
                "Paid Fee": paid_fee,
                "Pending Fee": remaining,
                "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.students.append(record)
            st.success("Student added successfully!")

# Display table
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    tab1, tab2 = st.tabs(["✅ Completed Fees", "⌛ Pending Fees"])

    with tab1:
        completed_df = df[df["Pending Fee"] == 0]
        if not completed_df.empty:
            st.dataframe(completed_df, use_container_width=True)
        else:
            st.info("No completed fee records yet.")

    with tab2:
        pending_df = df[df["Pending Fee"] > 0]
        if not pending_df.empty:
            st.dataframe(pending_df, use_container_width=True)
        else:
            st.info("All fees are completed! Great job!")
else:
    st.info("No student records yet. Add some!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Shruti Singh")