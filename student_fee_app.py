import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Student Fee Manager", layout="wide")

# Load or initialize data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Name", "Contact Number", "Class", "Installment 1", "Installment 2", "Installment 3", "Total Fee"])

df = load_data()

# Sidebar – Charts
with st.sidebar:
    st.subheader("Fee Analysis")
    if not df.empty:
        df["Paid Fee"] = df[["Installment 1", "Installment 2", "Installment 3"]].fillna(0).sum(axis=1)
        df["Pending Fee"] = df["Total Fee"] - df["Paid Fee"]

        pie = px.pie(df, values="Paid Fee", names="Name", title="Fee Distribution")
        st.plotly_chart(pie, use_container_width=True)

        bar = px.bar(df, x="Name", y=["Paid Fee", "Pending Fee"], barmode="group", title="Paid vs Pending")
        st.plotly_chart(bar, use_container_width=True)
    else:
        st.info("No data yet to display charts.")

st.title("🎓 Student Fee Management App")

# Search Functionality
search_name = st.text_input("🔍 Search by Name")
if search_name:
    result = df[df["Name"].str.contains(search_name, case=False)]
    if not result.empty:
        st.success("Student found!")
        st.dataframe(result)
    else:
        st.warning("No matching student found.")

# Add Student Form
with st.expander("➕ Add New Student"):
    with st.form("add_student"):
        name = st.text_input("Student Name")
        contact = st.text_input("Contact Number")
        student_class = st.text_input("Class")
        inst1 = st.number_input("Installment 1", value=0)
        inst2 = st.number_input("Installment 2", value=0)
        inst3 = st.number_input("Installment 3", value=0)
        total_fee = st.number_input("Total Fee", value=0)
        submit = st.form_submit_button("Add Student")

        if submit:
            new_data = pd.DataFrame([[name, contact, student_class, inst1, inst2, inst3, total_fee]],
                                    columns=["Name", "Contact Number", "Class", "Installment 1", "Installment 2", "Installment 3", "Total Fee"])
            df = pd.concat([df, new_data], ignore_index=True)
            st.success("Student added successfully.")
            st.experimental_rerun()

# Tabs for Paid and Pending Fee
tab1, tab2 = st.tabs(["✅ Paid", "❌ Pending"])

df["Paid Fee"] = df[["Installment 1", "Installment 2", "Installment 3"]].fillna(0).sum(axis=1)
df["Pending Fee"] = df["Total Fee"] - df["Paid Fee"]

with tab1:
    st.subheader("Students who Paid Fee")
    paid_df = df[df["Pending Fee"] <= 0]
    st.dataframe(paid_df)

with tab2:
    st.subheader("Students with Pending Fee")
    pending_df = df[df["Pending Fee"] > 0]
    st.dataframe(pending_df)

# Delete Student Section
with st.expander("🗑️ Delete Student"):
    name_to_delete = st.text_input("Enter Name to Delete")
    if st.button("Delete"):
        df = df[df["Name"] != name_to_delete]
        st.success(f"{name_to_delete} deleted successfully.")
        st.experimental_rerun()
