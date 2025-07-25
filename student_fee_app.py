import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Student Fee Manager", layout="wide")

# Theme toggle
theme = st.sidebar.radio("Select Theme", ("Light", "Dark"))

# Apply styles
if theme == "Dark":
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        .highlight-pending {
            background-color: #8B0000;
            color: #ffffff;
            font-weight: bold;
            font-size: 16px;
            padding: 0.3em;
            border-radius: 5px;
        }
        .highlight-completed {
            background-color: #006400;
            color: #ffffff;
            font-weight: bold;
            font-size: 16px;
            padding: 0.3em;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .highlight-pending {
            background-color: #ff9999;
            color: #000000;
            font-weight: bold;
            font-size: 16px;
            padding: 0.3em;
            border-radius: 5px;
        }
        .highlight-completed {
            background-color: #66cc66;
            color: #000000;
            font-weight: bold;
            font-size: 16px;
            padding: 0.3em;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

# Optional Pie Chart
st.subheader("📈 Overall Fee Distribution")
paid_total = df["Paid"].sum()
pending_total = df["Pending"].sum()

fig2 = go.Figure(data=[go.Pie(
    labels=['Paid', 'Pending'],
    values=[paid_total, pending_total],
    marker=dict(colors=['green', 'red']),
    hole=0.4
)])
st.plotly_chart(fig2, use_container_width=True)

# Data initialization
if 'students' not in st.session_state:
    st.session_state.students = []

# Add new student
st.title("💰 Student Fee Management App")
st.subheader("Add Student Details")

with st.form("student_form"):
    name = st.text_input("Student Name")
    contact = st.text_input("Contact Number")
    total_fee = st.number_input("Total Fee (₹)", min_value=0, value=0)
    installment1 = st.number_input("Installment 1", min_value=0, value=0)
    installment2 = st.number_input("Installment 2", min_value=0, value=0)
    installment3 = st.number_input("Installment 3", min_value=0, value=0)
    submit = st.form_submit_button("Add Student")

if submit:
    student = {
        "Name": name,
        "Contact": contact,
        "Total Fee": total_fee,
        "Installments": [installment1, installment2, installment3]
    }
    st.session_state.students.append(student)
    st.success(f"Student {name} added!")

# Show student list
st.subheader("🎓 All Students")
df_data = []
for student in st.session_state.students:
    paid = sum(student["Installments"])
    pending = max(0, student["Total Fee"] - paid)
    status = "Completed" if pending <= 0 else "Pending"
    df_data.append({
        "Name": student["Name"],
        "Contact": student["Contact"],
        "Total Fee": student["Total Fee"],
        "Paid": paid,
        "Pending": pending,
        "Status": status
    })

if df_data:
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)

    # Sidebar: show filtered lists
    st.sidebar.markdown("### ✅ Completed Students")
    for student in df[df["Status"] == "Completed"]["Name"]:
        st.sidebar.markdown(f"<div class='highlight-completed'>{student}</div>", unsafe_allow_html=True)

    st.sidebar.markdown("### ❌ Pending Students")
    for student in df[df["Status"] == "Pending"]["Name"]:
        st.sidebar.markdown(f"<div class='highlight-pending'>{student}</div>", unsafe_allow_html=True)

    # Fee Bar Chart
    st.subheader("📊 Fee Status Chart")
    fig = go.Figure(data=[
        go.Bar(name='Paid', x=df["Name"], y=df["Paid"], marker_color='green'),
        go.Bar(name='Pending', x=df["Name"], y=df["Pending"], marker_color='red')
    ])
    fig.update_layout(barmode='stack', xaxis_title="Students", yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)

# Watermark
st.markdown("<br><br><center style='opacity: 0.4;'>Made with ❤️ by Shruti Singh</center>", unsafe_allow_html=True)
