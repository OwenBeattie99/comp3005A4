import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database App")
        self.root.configure(bg='#FFCCCC')
        self.create_ui()

        # Initialize database connection
        self.connection = self.connect()

        # Display all students when the app starts
        self.get_all_students()

    def create_ui(self):
        # Entry fields for adding a new student
        self.first_name_label = ttk.Label(self.root, text="First Name:")
        self.first_name_entry = ttk.Entry(self.root)
        self.last_name_label = ttk.Label(self.root, text="Last Name:")
        self.last_name_entry = ttk.Entry(self.root)
        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_entry = ttk.Entry(self.root)
        self.enrollment_date_label = ttk.Label(self.root, text="Enrollment Date:")
        self.enrollment_date_entry = ttk.Entry(self.root)

        self.first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.email_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.enrollment_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.enrollment_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Button to add a new student
        self.add_button = ttk.Button(self.root, text="Add Student", command=self.add_student)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Entry field and button for updating a student
        self.update_label = ttk.Label(self.root, text="Update Student (Enter Student ID):")
        self.update_entry = ttk.Entry(self.root)
        self.update_button = ttk.Button(self.root, text="Update Email", command=self.update_student_email)

        self.update_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.update_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.update_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Entry field and button for deleting a student
        self.delete_label = ttk.Label(self.root, text="Delete Student (Enter Student ID):")
        self.delete_entry = ttk.Entry(self.root)
        self.delete_button = ttk.Button(self.root, text="Delete Student", command=self.delete_student)

        self.delete_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.delete_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.delete_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Listbox to display students
        self.student_listbox = tk.Listbox(self.root, height=10, width=80)
        self.student_listbox.grid(row=0, column=2, padx=10, pady=10, rowspan=9, columnspan=2)

        # Refresh button to reload student data
        self.refresh_button = ttk.Button(self.root, text="Refresh", command=self.get_all_students)
        self.refresh_button.grid(row=9, column=2, padx=10, pady=10, columnspan=2)





    # Connect to database using credentials
    def connect(self):
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="localhost",
                port="5433",
                database=""
            )
            return connection
        
        # Error handling 
        except Exception as e:
            print(f"Error: cant connect to the database. {e}")
            return None








    def get_all_students(self):
        if not self.connection:
            print("Error: Database connection not established.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students;")
            students = cursor.fetchall()

            # Clear the existing items in the listbox
            self.student_listbox.delete(0, tk.END)

            if not students:
                self.student_listbox.insert(tk.END, "No records found.")
            else:
                for student in students:
                    self.student_listbox.insert(tk.END, f"ID: {student[0]}, Name: {student[1]} {student[2]}, Email: {student[3]}, Enrollment Date: {student[4]}")

        except Exception as e:
            print(f"Error: Unable to retrieve students. {e}")

    def add_student(self):
        if not self.connection:
            messagebox.showerror("Error", "Database connection not established.")
            return

        # Get values from entry fields
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        enrollment_date = self.enrollment_date_entry.get()

        if not (first_name and last_name and email and enrollment_date):
            messagebox.showwarning("Warning", "All fields must be filled.")
            return

        try:
            cursor = self.connection.cursor()

            add_student_query = '''
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
            '''

            cursor.execute(add_student_query, (first_name, last_name, email, enrollment_date))
            new_student_id = cursor.fetchone()[0]
            self.connection.commit()

            # Display a success message
            messagebox.showinfo("Success", f"Student added successfully with ID: {new_student_id}.")

            # Refresh the listbox to show the updated student list
            self.get_all_students()

        except Exception as e:
            # Display an error message
            messagebox.showerror("Error", f"Unable to add student. {e}")

    def update_student_email(self):
        if not self.connection:
            messagebox.showerror("Error", "Database connection not established.")
            return

        # Get values from entry fields
        student_id = self.update_entry.get()
        new_email = self.email_entry.get()

        if not (student_id and new_email):
            messagebox.showwarning("Warning", "Please enter both student ID and new email.")
            return

        try:
            cursor = self.connection.cursor()

            update_email_query = '''
                UPDATE students
                SET email = %s
                WHERE student_id = %s;
            '''

            cursor.execute(update_email_query, (new_email, student_id))
            self.connection.commit()

            # Display a success message
            messagebox.showinfo("Success", "Email updated successfully.")

            # Refresh the listbox to show the updated student list
            self.get_all_students()

        except Exception as e:
            # Display an error message
            messagebox.showerror("Error", f"Unable to update email. {e}")

    def delete_student(self):
        if not self.connection:
            messagebox.showerror("Error", "Database connection not established.")
            return

        # Get value from entry field
        student_id = self.delete_entry.get()

        if not student_id:
            messagebox.showwarning("Warning", "Please enter student ID for deletion.")
            return

        try:
            cursor = self.connection.cursor()

            delete_student_query = '''
                DELETE FROM students
                WHERE student_id = %s;
            '''

            cursor.execute(delete_student_query, (student_id,))
            self.connection.commit()

            # Display a success message
            messagebox.showinfo("Success", "Student deleted successfully.")

            # Refresh the listbox to show the updated student list
            self.get_all_students()

        except Exception as e:
            # Display an error message
            messagebox.showerror("Error", f"Unable to delete student. {e}")

def main():
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
