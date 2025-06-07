import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def create_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    cohort TEXT NOT NULL,
                    comp_arch TEXT,
                    networking TEXT,
                    r_programming TEXT
                )''')
    conn.commit()
    conn.close()

create_db()

def create():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS login (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

create()


# Variable to track login success


# Variable to track login success
login_success = False

# Function to initialize the database and create the users table

def initialize_database():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Function to validate login
def validate_login(username, password):
    global login_success
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    row = cur.fetchone()
    if row:
        login_success = True
        messagebox.showinfo("Login Successful", "Welcome!")
        login_window.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")
    conn.close()

# Function to add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "User added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    finally:
        conn.close()

# Function to handle the add user button click event
def on_add_user_button_click():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        add_user(username, password)
    else:
        messagebox.showerror("Error", "Please enter both username and password")

# Function to create the login window
def create_login_window():
    global login_window, username_entry, password_entry
    login_window = tk.Tk()
    login_window.title("Login Screen")
    
    # Username label and entry
    username_label = tk.Label(login_window, text="Username")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    # Password label and entry
    password_label = tk.Label(login_window, text="Password")
    password_label.pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()

    # Login button
    login_button = tk.Button(login_window, text="Login", 
                             command=lambda: validate_login(username_entry.get(), password_entry.get()))
    login_button.pack()

    # Add User button
    add_user_button = tk.Button(login_window, text="Add User", command=on_add_user_button_click)
    add_user_button.pack()

    login_window.mainloop()
# Run the main event loop



class RegistrationForm(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Student Management System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (HomePage, Mark, View):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Home Page", font=("Arial", 16))
        label.pack(pady=10)
        
        self.student_count_label = tk.Label(self, text="", font=("Arial", 12))
        self.student_count_label.pack(pady=10)
        
        register_button = ttk.Button(self, text="Register Student", command=lambda: controller.show_frame(Mark))
        register_button.pack(pady=5)
        
        view_button = ttk.Button(self, text="View Students", command=lambda: controller.show_frame(View))
        view_button.pack(pady=5)

        self.update_student_count()

    def update_student_count(self):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM students")
        count = c.fetchone()[0]
        conn.close()
        self.student_count_label.config(text=f"Number of Students: {count}")

# Main 

class Mark(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Input Mark", font=("Arial", 16))
        label.pack(pady=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        button1.pack(pady=5)

        # Create a form layout for the fields
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10)

        # Adding input fields for student data
        self.label1 = tk.Label(form_frame, text="Student First Name:")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry1 = tk.Entry(form_frame)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        self.label2 = tk.Label(form_frame, text="Student Last Name:")
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry2 = tk.Entry(form_frame)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        self.label3 = tk.Label(form_frame, text="Student ID:")
        self.label3.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry3 = tk.Entry(form_frame)
        self.entry3.grid(row=2, column=1, padx=5, pady=5)

        self.label4 = tk.Label(form_frame, text="Cohort:")
        self.label4.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry4 = tk.Entry(form_frame)
        self.entry4.grid(row=3, column=1, padx=5, pady=5)

        self.label5 = tk.Label(form_frame, text="Computer Architecture:")
        self.label5.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry5 = tk.Entry(form_frame)
        self.entry5.grid(row=4, column=1, padx=5, pady=5)

        self.label6 = tk.Label(form_frame, text="Networking:")
        self.label6.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry6 = tk.Entry(form_frame)
        self.entry6.grid(row=5, column=1, padx=5, pady=5)

        self.label7 = tk.Label(form_frame, text="R programming:")
        self.label7.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry7 = tk.Entry(form_frame)
        self.entry7.grid(row=6, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack(pady=10)

        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_data)
        self.delete_button.pack(pady=10)

    def save_data(self):
        student_first_name = self.entry1.get()
        student_last_name = self.entry2.get()
        student_id = self.entry3.get()
        cohort = self.entry4.get()
        comp_arch = self.entry5.get()
        networking = self.entry6.get()
        r_programming = self.entry7.get()

        message = f"Name: {student_first_name} \nLast Name: {student_last_name} \nStudent ID: {student_id} \nCohort: {cohort}"
        messagebox.showinfo("Student Information have been saved", message)

        conn = sqlite3.connect('students.db')
        c = conn.cursor()

        # Check for existing student
        c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        existing_student = c.fetchone()

        if existing_student:
            messagebox.showerror("Error", "Student with the same ID already exists.")
        else:
            c.execute("INSERT INTO students (id, first_name, last_name, cohort, comp_arch, networking, r_programming) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (student_id, student_first_name, student_last_name, cohort, comp_arch, networking, r_programming))
            conn.commit()
            messagebox.showinfo("Success", "Student data saved successfully!")

        conn.close()
        
        # Update the student count on the home page
        self.controller.frames[HomePage].update_student_count()

    def delete_data(self):
        student_id = self.entry3.get()

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student data deleted successfully!")
        
        # Update the student count on the home page
        self.controller.frames[HomePage].update_student_count()




class View(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="View Students", font=("Arial", 16))
        label.pack(pady=10)
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        button1.pack(pady=5)

        self.tree = ttk.Treeview(self, columns=('ID', 'First Name', 'Last Name', 'Cohort', 'Comp Arch', 'Networking', 'R Programming'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('First Name', text='First Name')
        self.tree.heading('Last Name', text='Last Name')
        self.tree.heading('Cohort', text='Cohort')
        self.tree.heading('Comp Arch', text='Comp Arch')
        self.tree.heading('Networking', text='Networking')
        self.tree.heading('R Programming', text='R Programming')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.refresh_data()

        open_button = ttk.Button(self, text="Refresh Data", command=self.refresh_data)
        open_button.pack(pady=10)

        search_label = tk.Label(self, text="Search by ID or Name:")
        search_label.pack(pady=5)
        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=5)
        search_button = ttk.Button(self, text="Search", command=self.search_data)
        search_button.pack(pady=5)

        delete_button = ttk.Button(self, text="Delete", command=self.delete_data)
        delete_button.pack(pady=5)

        update_button = ttk.Button(self, text="Update", command=self.update_data)
        update_button.pack(pady=5)

        graph_button = ttk.Button(self, text="Show Graph", command=self.show_graph)
        graph_button.pack(pady=5)

    def refresh_data(self):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        rows = c.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_data(self):
        search_term = self.search_entry.get()
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE first_name LIKE ? OR last_name LIKE ? OR id = ?", ('%' + search_term + '%', '%' + search_term + '%', search_term))
        rows = c.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def delete_data(self):
        selected_items = self.tree.selection()
        if selected_items:
            for selected_item in selected_items:
                values = self.tree.item(selected_item, 'values')
                student_id = values[0]

                conn = sqlite3.connect('students.db')
                c = conn.cursor()
                c.execute("DELETE FROM students WHERE id = ?", (student_id,))
                conn.commit()
                conn.close()

                self.tree.delete(selected_item)

            messagebox.showinfo("Info", "Selected student data deleted successfully.")

    def update_data(self):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, 'values')
            self.show_update_window(values)

    def show_update_window(self, values):
        update_window = tk.Toplevel(self)
        update_window.title("Update Student Information")

        fields = ['First Name', 'Last Name', 'Cohort', 'Comp Arch', 'Networking', 'R Programming']
        entries = {}

        for idx, field in enumerate(fields):
            label = tk.Label(update_window, text=field)
            label.grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(update_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry.insert(0, values[idx + 1])
            entries[field] = entry

        def save_changes():
            updated_values = [entries[field].get() for field in fields]
            self.update_db(values[0], updated_values)
            self.refresh_data()
            update_window.destroy()

        save_button = ttk.Button(update_window, text="Save", command=save_changes)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def update_db(self, student_id, updated_values):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('''UPDATE students SET first_name = ?, last_name = ?, cohort = ?, comp_arch = ?, networking = ?, r_programming = ?
                     WHERE id = ?''',
                  (*updated_values, student_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Student data updated successfully.")

    def show_graph(self):
        cohorts = {}
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            cohort = row[3]
            if cohort not in cohorts:
                cohorts[cohort] = {'students': 0, 'Comp Arch': 0, 'Networking': 0, 'R Programming': 0}
            cohorts[cohort]['students'] += 1
            cohorts[cohort]['Comp Arch'] += float(row[4])
            cohorts[cohort]['Networking'] += float(row[5])
            cohorts[cohort]['R Programming'] += float(row[6])

        graph_window = tk.Toplevel(self)
        graph_window.title("Average Marks per Subject by Cohort")

        fig, ax = plt.subplots(figsize=(10, 5))
        labels = []
        ca_marks = []
        net_marks = []
        rp_marks = []

        for cohort, data in cohorts.items():
            labels.append(cohort)
            ca_marks.append(data['Comp Arch'] / data['students'])
            net_marks.append(data['Networking'] / data['students'])
            rp_marks.append(data['R Programming'] / data['students'])

        x = range(len(labels))
        ax.bar(x, ca_marks, width=0.2, label='Comp Arch', align='center')
        ax.bar([p + 0.2 for p in x], net_marks, width=0.2, label='Networking', align='center')
        ax.bar([p + 0.4 for p in x], rp_marks, width=0.2, label='R Programming', align='center')

        ax.set_xticks([p + 0.2 for p in x])
        ax.set_xticklabels(labels)
        ax.set_xlabel('Cohorts')
        ax.set_ylabel('Average Marks')
        ax.set_title('Average Marks per Subject by Cohort')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Main Application


initialize_database()
create_login_window()

if login_success:
    app = RegistrationForm()
    app.mainloop()
else:
    messagebox.showerror("Access Denied", "You must log in to access the application.")
    



# Function to initialize the database and create the users table
