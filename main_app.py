import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    course TEXT,
    semester INTEGER,
    email TEXT,
    phone TEXT
)
""")
conn.commit()

# -----------------------------
# Functions
# -----------------------------
def add_student(name, age, gender, course, semester, email, phone):
    cursor.execute("""
    INSERT INTO students(name, age, gender, course, semester, email, phone)
    VALUES(?,?,?,?,?,?,?)
    """, (name, age, gender, course, semester, email, phone))
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    return rows


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


def update_student(student_id, name, age, gender, course, semester, email, phone):
    cursor.execute("""
    UPDATE students
    SET name=?, age=?, gender=?, course=?, semester=?, email=?, phone=?
    WHERE id=?
    """, (name, age, gender, course, semester, email, phone, student_id))
    conn.commit()


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student"
]

choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Home
# -----------------------------
if choice == "Home":

    st.header("Welcome")

    st.write("""
This application allows you to:

- Add Student Records
- View Student Records
- Update Existing Records
- Delete Records
- Store data using SQLite Database
""")

# -----------------------------
# Add Student
# -----------------------------
elif choice == "Add Student":

    st.header("Add New Student")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name")
        age = st.number_input("Age", 15, 50)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        course = st.text_input("Course")

    with col2:
        semester = st.number_input("Semester", 1, 12)
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")

    if st.button("Add Student"):

        if name == "":
            st.error("Student name required")

        else:
            add_student(
                name,
                age,
                gender,
                course,
                semester,
                email,
                phone
            )
            st.success("Student Added Successfully")

# -----------------------------
# View Students
# -----------------------------
elif choice == "View Students":

    st.header("Student Records")

    data = view_students()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Course",
            "Semester",
            "Email",
            "Phone"
        ]
    )

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

# -----------------------------
# Update Student
# -----------------------------
elif choice == "Update Student":

    st.header("Update Student")

    data = view_students()

    ids = [row[0] for row in data]

    if len(ids) == 0:
        st.warning("No student records found.")

    else:

        student_id = st.selectbox("Select Student ID", ids)

        selected = None

        for row in data:
            if row[0] == student_id:
                selected = row

        name = st.text_input("Name", selected[1])
        age = st.number_input("Age", 15, 50, selected[2])
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(selected[3])
        )

        course = st.text_input("Course", selected[4])

        semester = st.number_input(
            "Semester",
            1,
            12,
            selected[5]
        )

        email = st.text_input("Email", selected[6])

        phone = st.text_input("Phone", selected[7])

        if st.button("Update"):

            update_student(
                student_id,
                name,
                age,
                gender,
                course,
                semester,
                email,
                phone
            )

            st.success("Record Updated Successfully")

# -----------------------------
# Delete Student
# -----------------------------
elif choice == "Delete Student":

    st.header("Delete Student")

    data = view_students()

    ids = [row[0] for row in data]

    if len(ids) == 0:

        st.warning("No records available.")

    else:

        student_id = st.selectbox("Student ID", ids)

        if st.button("Delete"):

            delete_student(student_id)

            st.success("Record Deleted Successfully")

# -----------------------------
# Footer
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.info("Student Record Management System\nUsing Streamlit + SQLite")
