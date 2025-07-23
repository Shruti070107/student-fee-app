import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state if not already done
if 'students' not in st.session_state:
    st.session_state.students = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Page config
st.set_page_config(page_title="Student Fee Manager", layout="wide")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.session_state.dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode, help="Switch to dark or light theme")
    st.session_state.search_query = st.text_input("🔍 Search by Name or Contact")

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

# Summary Section
if st.session_state.students:
    df_summary = pd.DataFrame(st.session_state.students)
    total_students = len(df_summary)
    total_fee = df_summary['Total Fee'].sum()
    total_paid = df_summary['Paid Fee'].sum()
    total_pending = df_summary['Pending Fee'].sum()

    st.markdown("### 📊 Fee Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Students", total_students)
    col2.metric("💰 Total Fee", f"₹{total_fee}")
    col3.metric("✅ Total Paid", f"₹{total_paid}")
    col4.metric("⌛ Total Pending", f"₹{total_pending}")
    st.markdown("---")

# Form to add/edit students
with st.expander("➕ Add New Student"):
    with st.form("student_form"):
        name = st.text_input("Student Name")
        contact = st.text_input("Contact Number")
        class_ = st.number_input("Class", step=1, min_value=1)
        inst1 = st.number_input("Installment 1", min_value=0)
        inst2 = st.number_input("Installment 2", min_value=0)
        inst3 = st.number_input("Installment 3 (Optional)", min_value=0)
        submit = st.form_submit_button("Save Student")

        if submit and name and contact:
            total_paid = inst1 + inst2 + inst3
            total_fee = total_paid  # Fee assumed to be sum of installments
            remaining = total_fee - total_paid
            record = {
                "Name": name,
                "Contact No": contact,
                "Class": class_,
                "Installment 1": inst1,
                "Installment 2": inst2,
                "Installment 3": inst3,
                "Total Fee": total_fee,
                "Paid Fee": total_paid,
                "Pending Fee": remaining,
                "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.students.append(record)
            st.success("Student added successfully!")

# Display table if students exist
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    # Search filter
    query = st.session_state.search_query.lower()
    if query:
        df = df[df['Name'].str.lower().str.contains(query) | df['Contact No'].str.contains(query)]

    tab1, tab2 = st.tabs(["✅ Completed Fees", "⌛ Pending Fees"])

    with tab1:
        completed_df = df[df["Pending Fee"] == 0].copy()
        if not completed_df.empty:
            st.dataframe(completed_df, use_container_width=True)
        else:
            st.info("No completed fee records yet.")

    with tab2:
        pending_df = df[df["Pending Fee"] > 0].copy()
        if not pending_df.empty:
            st.dataframe(pending_df, use_container_width=True)
        else:
            st.info("All fees are completed! Great job!")

    # Delete section
    with st.expander("🗑️ Delete a Student"):
        names = [s['Name'] for s in st.session_state.students]
        selected = st.selectbox("Select student to delete", options=names)
        if st.button("Delete Student"):
            st.session_state.students = [s for s in st.session_state.students if s['Name'] != selected]
            st.success(f"Deleted student: {selected}")
else:
    st.info("No student records yet. Add some!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Shruti Singh")
