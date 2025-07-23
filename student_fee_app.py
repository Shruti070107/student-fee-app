import tkinter as tk
from tkinter import messagebox

# Main Window
root = tk.Tk()
root.title("Student Fee Manager")
root.geometry("950x650")
root.configure(bg="#f0f4ff")

students = []

def clear_entries():
    for entry in entries:
        entry.delete(0, tk.END)

def calculate_summary():
    total_students = len(students)
    paid = sum(1 for s in students if sum(s["fees"]) >= s["total"])
    pending = total_students - paid
    summary_label.config(text=f"👥 Total: {total_students} | ✅ Paid: {paid} | ⚠️ Pending: {pending}")

def refresh_display():
    pending_box.configure(state="normal")
    completed_box.configure(state="normal")
    pending_box.delete("1.0", "end")
    completed_box.delete("1.0", "end")

    sorted_students = sorted(students, key=lambda s: s["name"].lower())

    for student in sorted_students:
        name, contact, fees = student["name"], student["contact"], student["fees"]
        total_paid = sum(fees)
        total_required = student["total"]
        balance = total_required - total_paid

        info = (
            f"Name: {name}\n"
            f"Contact: {contact}\n"
            f"Installments: {fees}\n"
            f"Paid: ₹{total_paid} / ₹{total_required}\n"
            f"Balance: ₹{balance if balance > 0 else 0}\n\n"
        )

        if total_paid >= total_required:
            completed_box.insert("end", info)
        else:
            pending_box.insert("end", info)

    calculate_summary()
    pending_box.configure(state="disabled")
    completed_box.configure(state="disabled")

def add_student():
    name = name_entry.get()
    contact = contact_entry.get()
    try:
        inst1 = float(inst1_entry.get()) if inst1_entry.get() else 0
        inst2 = float(inst2_entry.get()) if inst2_entry.get() else 0
        inst3 = float(inst3_entry.get()) if inst3_entry.get() else 0
        total = float(total_entry.get()) if total_entry.get() else 0
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for installments and total.")
        return

    if not name or not contact or not total:
        messagebox.showerror("Missing Info", "Please fill in all the required fields.")
        return

    students.append({"name": name, "contact": contact, "fees": [inst1, inst2, inst3], "total": total})
    clear_entries()
    refresh_display()

def delete_student():
    name = name_entry.get()
    for s in students:
        if s["name"].lower() == name.lower():
            students.remove(s)
            messagebox.showinfo("Deleted", f"Record of {name} deleted.")
            clear_entries()
            refresh_display()
            return
    messagebox.showerror("Not Found", "Student not found.")

def update_student():
    name = name_entry.get()
    for s in students:
        if s["name"].lower() == name.lower():
            try:
                s["contact"] = contact_entry.get()
                s["fees"] = [
                    float(inst1_entry.get()) if inst1_entry.get() else 0,
                    float(inst2_entry.get()) if inst2_entry.get() else 0,
                    float(inst3_entry.get()) if inst3_entry.get() else 0,
                ]
                s["total"] = float(total_entry.get()) if total_entry.get() else 0
                messagebox.showinfo("Updated", f"Details for {name} updated.")
                clear_entries()
                refresh_display()
                return
            except ValueError:
                messagebox.showerror("Invalid Input", "Check installment and total fee values.")
                return
    messagebox.showerror("Not Found", "Student not found.")

# UI Labels
fields = ["Name", "Contact Number", "Installment 1", "Installment 2", "Installment 3", "Total Fees"]
entries = []

for idx, label in enumerate(fields):
    tk.Label(root, text=label, bg="#f0f4ff", font=("Arial", 11, "bold")).grid(row=idx, column=0, padx=10, pady=5, sticky="w")

name_entry = tk.Entry(root)
contact_entry = tk.Entry(root)
inst1_entry = tk.Entry(root)
inst2_entry = tk.Entry(root)
inst3_entry = tk.Entry(root)
total_entry = tk.Entry(root)

entries = [name_entry, contact_entry, inst1_entry, inst2_entry, inst3_entry, total_entry]

for i, entry in enumerate(entries):
    entry.grid(row=i, column=1, padx=5, pady=5, ipadx=30)

    def focus_next(event, idx=i):
        if idx + 1 < len(entries):
            entries[idx + 1].focus()
    entry.bind("<Return>", focus_next)

# Buttons
tk.Button(root, text="Add Student", command=add_student, bg="#4caf50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=20)
tk.Button(root, text="Update Student", command=update_student, bg="#2196f3", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=20)
tk.Button(root, text="Delete Student", command=delete_student, bg="#f44336", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=20)

# Summary Label
summary_label = tk.Label(root, text="👥 Total: 0 | ✅ Paid: 0 | ⚠️ Pending: 0", bg="#f0f4ff", font=("Arial", 11, "bold"))
summary_label.place(x=310, y=220)

# Pending & Completed Boxes
tk.Label(root, text="Pending Fees", bg="#f0f4ff", fg="red", font=("Arial", 12, "bold")).place(x=50, y=260)
pending_box = tk.Text(root, height=15, width=40, bg="#fff4f4", font=("Arial", 10))
pending_box.place(x=50, y=290)

tk.Label(root, text="Fees Completed", bg="#f0f4ff", fg="green", font=("Arial", 12, "bold")).place(x=480, y=260)
completed_box = tk.Text(root, height=15, width=40, bg="#f4fff4", font=("Arial", 10))
completed_box.place(x=480, y=290)

root.mainloop()