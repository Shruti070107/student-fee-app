import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Fee Management", layout="wide")

st.title("🎓 Student Fee Management App")

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = []

def calculate_status(total, i1, i2, i3):
    paid = i1 + i2 + i3
    if paid >= total:
        return "Completed"
    return "Pending"

def add_student(name, roll_no, course, total, i1, i2, i3):
    status = calculate_status(total, i1, i2, i3)
    student = {
        "Name": name,
        "Roll No": roll_no,
        "Course": course,
        "Total Fees": total,
        "1st Installment": i1,
        "2nd Installment": i2,
        "3rd Installment": i3,
        "Status": status
    }
    st.session_state.students.append(student)

def update_student(index, name, roll_no, course, total, i1, i2, i3):
    status = calculate_status(total, i1, i2, i3)
    st.session_state.students[index] = {
        "Name": name,
        "Roll No": roll_no,
        "Course": course,
        "Total Fees": total,
        "1st Installment": i1,
        "2nd Installment": i2,
        "3rd Installment": i3,
        "Status": status
    }

def delete_student(index):
    del st.session_state.students[index]

st.sidebar.header("➕ Add or Update Student")

# Form Inputs
with st.sidebar.form("student_form"):
    name = st.text_input("Student Name")
    roll_no = st.text_input("Roll No")
    course = st.text_input("Course")
    total_fees = st.number_input("Total Fees", min_value=0)
    i1 = st.number_input("1st Installment", min_value=0)
    i2 = st.number_input("2nd Installment", min_value=0)
    i3 = st.number_input("3rd Installment", min_value=0)
    
    edit_index = st.selectbox("Select student to update (optional)", options=["New"] + [s["Name"] for s in st.session_state.students])
    submitted = st.form_submit_button("Save")

    if submitted:
        if edit_index == "New":
            add_student(name, roll_no, course, total_fees, i1, i2, i3)
            st.success(f"✅ Added student: {name}")
        else:
            idx = [s["Name"] for s in st.session_state.students].index(edit_index)
            update_student(idx, name, roll_no, course, total_fees, i1, i2, i3)
            st.success(f"✏️ Updated student: {name}")

# Display Table
st.subheader("📋 Student Fee Records")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df, use_container_width=True)

    for i, student in enumerate(st.session_state.students):
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button(f"🗑️ Delete {student['Name']}", key=f"del_{i}"):
                delete_student(i)
                st.rerun()
else:
    st.info("No students added yet.")