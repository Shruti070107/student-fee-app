import streamlit as st
import pandas as pd
import plotly.express as px
import uuid

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []

# Sidebar with theme toggle and chart
st.sidebar.title("Options")
theme = st.sidebar.radio("Select Theme", ("Light", "Dark"))
st.markdown(f"""<style>
    .reportview-container {{
        background-color: {'#1e1e1e' if theme == 'Dark' else 'white'};
        color: {'white' if theme == 'Dark' else 'black'};
    }}
</style>""", unsafe_allow_html=True)

# Title
st.title("🎓 Student Fee Management App")

# Form for student data
with st.form("fee_form"):
    name = st.text_input("Student Name")
    contact = st.text_input("Contact Number")
    student_class = st.number_input("Class", min_value=1, step=1)
    installment1 = st.number_input("Installment 1", min_value=0.0, step=100.0)
    installment2 = st.number_input("Installment 2", min_value=0.0, step=100.0)
    installment3 = st.number_input("Installment 3", min_value=0.0, step=100.0)
    pending_fee = st.number_input("Pending Fee", min_value=0.0, step=100.0)
    submitted = st.form_submit_button("Add/Update Record")

    if submitted:
        paid_fee = installment1 + installment2 + installment3
        total_fee = paid_fee + pending_fee
        student_id = str(uuid.uuid4())

        st.session_state.data.append({
            "ID": student_id,
            "Name": name,
            "Contact": contact,
            "Class": int(student_class),
            "Installment 1": installment1,
            "Installment 2": installment2,
            "Installment 3": installment3,
            "Paid Fee": paid_fee,
            "Pending Fee": pending_fee,
            "Total Fee": total_fee
        })
        st.success("Student record added successfully!")

# Search bar
search_query = st.text_input("🔍 Search Student by Name")

# Data filtering
df = pd.DataFrame(st.session_state.data)

if not df.empty:
    if search_query:
        df = df[df['Name'].str.contains(search_query, case=False, na=False)]
        st.subheader("Search Results")
    else:
        st.subheader("All Student Records")

    # Tabs for Paid and Pending
    tab1, tab2 = st.tabs(["✅ Fees Completed", "❗ Fees Pending"])

    with tab1:
        paid_df = df[df['Pending Fee'] == 0]
        st.dataframe(paid_df, use_container_width=True)

    with tab2:
        pending_df = df[df['Pending Fee'] > 0]
        st.dataframe(pending_df, use_container_width=True)

    # Delete button with highlight
    for idx, row in df.iterrows():
        col1, col2 = st.columns([8, 2])
        with col1:
            st.write(f"**{row['Name']} ({row['Contact']})** - Class {row['Class']} | Total: ₹{row['Total Fee']} | Pending: ₹{row['Pending Fee']}")
        with col2:
            if st.button("❌ Delete", key=row['ID']):
                st.session_state.data = [r for r in st.session_state.data if r['ID'] != row['ID']]
                st.success(f"Deleted record for {row['Name']}")
                st.experimental_rerun()

    # Charts and analysis in sidebar
    st.sidebar.subheader("📊 Fee Analysis")
    if len(df) > 0:
        fig = px.pie(df, names="Name", values="Pending Fee", title="Pending Fees Share")
        st.sidebar.plotly_chart(fig, use_container_width=True)

        bar_fig = px.bar(df, x="Name", y=["Paid Fee", "Pending Fee"], barmode='group', title="Fees Paid vs Pending")
        st.sidebar.plotly_chart(bar_fig, use_container_width=True)
else:
    st.info("No records found. Please add a student above.")
