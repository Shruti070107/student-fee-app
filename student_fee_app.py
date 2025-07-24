import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Student Fee Management", layout="wide")

# Initialize session state for data
if "students" not in st.session_state:
    st.session_state.students = []

# Theme Toggle
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        .highlight-pending {
            background-color: #660000;
            color: white;
            padding: 0.3em;
            border-radius: 5px;
        }
        .highlight-completed {
            background-color: #003300;
            color: white;
            padding: 0.3em;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .highlight-pending {
            background-color: #ffe6e6;
            padding: 0.3em;
            border-radius: 5px;
        }
        .highlight-completed {
            background-color: #e6ffe6;
            padding: 0.3em;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

# Title
st.title("📘 Student Fee Management App")
st.markdown("<div style='text-align:right;color:grey;'>Made by Shruti Singh</div>", unsafe_allow_html=True)

# Add Student Form
with st.form("Add Student"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name")
        contact = st.text_input("Contact No")
        class_name = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        total_fee = st.number_input("Total Fee", min_value=0, value=0)
    with col2:
        installment_1 = st.number_input("Installment 1", min_value=0, value=0)
        installment_2 = st.number_input("Installment 2", min_value=0, value=0)
        installment_3 = st.number_input("Installment 3 (Optional)", min_value=0, value=0)

    submitted = st.form_submit_button("Add Student")
    if submitted and name and contact:
        paid = installment_1 + installment_2 + installment_3
        pending = total_fee - paid
        st.session_state.students.append({
            "Name": name,
            "Contact": contact,
            "Class": class_name,
            "Installment 1": installment_1,
            "Installment 2": installment_2,
            "Installment 3": installment_3,
            "Total Fee": total_fee,
            "Paid Fee": paid,
            "Pending Fee": pending
        })
        st.success("Student added successfully!")

# Search
search_name = st.text_input("🔍 Search Student by Name")

# Display Students
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    if search_name:
        df = df[df["Name"].str.contains(search_name, case=False, na=False)]

    for i, student in df.iterrows():
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
        with col1:
            st.markdown(f"**{student['Name']} ({student['Contact']}) - Class {student['Class']}**")
        with col2:
            st.markdown(f"<div class='highlight-completed'>Paid: ₹{student['Paid Fee']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='highlight-pending'>Pending: ₹{student['Pending Fee']}</div>", unsafe_allow_html=True)
        with col4:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.students.pop(i)
                st.experimental_rerun()

    st.dataframe(df, use_container_width=True)

    # Sidebar Metrics
    total_collected = sum(s["Paid Fee"] for s in st.session_state.students)
    total_pending = sum(s["Pending Fee"] for s in st.session_state.students)
    st.sidebar.metric("Total Fees Collected", f"₹ {total_collected}")
    st.sidebar.metric("Total Fees Pending", f"₹ {total_pending}")

    # Pie Chart
    chart_df = pd.DataFrame({
        "Status": ["Collected", "Pending"],
        "Amount": [total_collected, total_pending]
    })
    st.sidebar.plotly_chart(px.pie(chart_df, values='Amount', names='Status', title='Fee Distribution'), use_container_width=True)

    # Sidebar Lists
    with st.sidebar.expander("📌 Pending Students"):
        for student in st.session_state.students:
            if student["Pending Fee"] > 0:
                st.markdown(f"<span style='color:#ffcccc;'>{student['Name']} (₹{student['Pending Fee']})</span>", unsafe_allow_html=True)

    with st.sidebar.expander("✅ Completed Students"):
        for student in st.session_state.students:
            if student["Pending Fee"] <= 0:
                st.markdown(f"<span style='color:#ccffcc;'>{student['Name']}</span>", unsafe_allow_html=True)
else:
    st.info("No student records yet.")