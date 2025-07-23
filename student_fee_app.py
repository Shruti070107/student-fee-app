
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CSV file
CSV_FILE = "students.csv"

# Load or initialize
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Contact No", "Fee Status"])
    df.to_csv(CSV_FILE, index=False)
else:
    df = pd.read_csv(CSV_FILE)

# Page config
st.set_page_config(page_title="Student Fee Manager", layout="wide")

# Theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

colors = {
    "light": {"bg": "#f5f7fa", "text": "#000", "box": "#fff"},
    "dark": {"bg": "#0e1117", "text": "#fff", "box": "#1e1e1e"},
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {colors[st.session_state.theme]['bg']};
        color: {colors[st.session_state.theme]['text']};
    }}
    .stTextInput > div > div > input {{
        background-color: {colors[st.session_state.theme]['box']} !important;
        color: {colors[st.session_state.theme]['text']} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Theme
st.title("🎓 Student Fee Management App")
st.button("🌗 Toggle Theme", on_click=toggle_theme)

# Sidebar - Add/Edit
st.sidebar.header("➕ Add / Edit Student")
name = st.sidebar.text_input("Student Name")
contact = st.sidebar.text_input("Contact No")
status = st.sidebar.selectbox("Fee Status", ["Pending", "Completed"])

if st.sidebar.button("💾 Save"):
    if name and contact:
        match = df[(df["Name"] == name) & (df["Contact No"] == contact)]
        if not match.empty:
            df.loc[match.index, "Fee Status"] = status
            st.sidebar.success("✅ Updated successfully")
        else:
            df = pd.concat([df, pd.DataFrame([{"Name": name, "Contact No": contact, "Fee Status": status}])], ignore_index=True)
            st.sidebar.success("✅ Added successfully")
        df.to_csv(CSV_FILE, index=False)
    else:
        st.sidebar.warning("⚠️ Fill all fields")

# Sidebar - Delete
st.sidebar.markdown("---")
st.sidebar.header("🗑️ Delete Student")
del_name = st.sidebar.text_input("Name to Delete")

if st.sidebar.button("❌ Delete"):
    before = df.shape[0]
    df = df[df["Name"] != del_name]
    after = df.shape[0]
    if before == after:
        st.sidebar.warning("⚠️ No match found")
    else:
        df.to_csv(CSV_FILE, index=False)
        st.sidebar.success("🗑️ Deleted")

# Main - Status Views
st.subheader("📋 Fee Status Overview")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❌ Pending Fees")
    st.dataframe(df[df["Fee Status"] == "Pending"], use_container_width=True)

with col2:
    st.markdown("### ✅ Completed Fees")
    st.dataframe(df[df["Fee Status"] == "Completed"], use_container_width=True)

# Footer
st.markdown("---")
st.caption(f"© {datetime.now().year} Shruti Singh | Built with ❤️ using Streamlit")
