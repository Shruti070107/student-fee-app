import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

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

    if st.session_state.students:
        df_all = pd.DataFrame(st.session_state.students)
        st.markdown("### 📈 Fee Distribution")
        fig = px.pie(df_all, values='Paid Fee', names='Name', title='Paid Fee Distribution', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

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
    total_fee = df_summary['Installment 1'].sum() + df_summary['Installment 2'].sum() + df_summary['Installment 3'].sum()
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
            st.experimental_rerun()

# Display table if students exist
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    # Search filter
    query = st.session_state.search_query.lower()
    highlight_name = None
    if query:
        matched = df[df['Name'].str.lower().str.contains(query) | df['Contact No'].str.contains(query)]
        if not matched.empty:
            st.markdown("### 🔍 Search Result")
            highlight_name = matched.iloc[0]['Name']
            st.dataframe(matched.style.apply(lambda x: ['background-color: #ffcccc' if x['Name'] == highlight_name else '' for _ in x], axis=1), use_container_width=True)
        else:
            st.warning("No match found.")

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
        highlight_style = "color: red; font-weight: bold;" if highlight_name in names else ""
        delete_container = st.container()
        with delete_container:
            selected = st.selectbox("Select student to delete", options=names, index=names.index(highlight_name) if highlight_name in names else 0, format_func=lambda x: f"🔴 {x}" if x == highlight_name else x)
            if st.button("Delete Student"):
                st.session_state.students = [s for s in st.session_state.students if s['Name'] != selected]
                st.success(f"Deleted student: {selected}")
                st.experimental_rerun()
else:
    st.info("No student records yet. Add some!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Shruti Singh")
