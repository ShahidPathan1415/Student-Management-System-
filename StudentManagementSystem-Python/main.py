import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from database import get_connection

NAVY = "#13284B"
BLUE = "#306CE5"
GREEN = "#2B9A66"
RED = "#CD4A4A"
LIGHT = "#F5F8FC"
TEXT = "#232D3D"
MUTED = "#666666"


class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StudentHub")
        self.geometry("1100x650")
        self.minsize(900, 550)
        self.configure(bg=LIGHT)
        self.selected_id = None
        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        self.geometry("700x430")
        outer = tk.Frame(self, bg=LIGHT)
        outer.pack(fill="both", expand=True)
        left = tk.Frame(outer, bg=NAVY, width=320)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)
        tk.Label(left, text="StudentHub", font=("Arial", 25, "bold"), fg="white", bg=NAVY).place(relx=.5, rely=.42, anchor="center")
        tk.Label(left, text="Manage student records\nsimply and securely.", justify="center", font=("Arial", 13), fg="#DCE6F8", bg=NAVY).place(relx=.5, rely=.56, anchor="center")
        form = tk.Frame(outer, bg=LIGHT, padx=55, pady=65)
        form.pack(side="right", fill="both", expand=True)
        tk.Label(form, text="Welcome back", font=("Arial", 24, "bold"), fg=TEXT, bg=LIGHT).pack(anchor="w")
        tk.Label(form, text="Sign in to your administrator account", fg=MUTED, bg=LIGHT).pack(anchor="w", pady=(3, 22))
        tk.Label(form, text="Username", fg=TEXT, bg=LIGHT, font=("Arial", 11, "bold")).pack(anchor="w")
        self.username = ttk.Entry(form, font=("Arial", 12)); self.username.pack(fill="x", pady=(4, 14))
        tk.Label(form, text="Password", fg=TEXT, bg=LIGHT, font=("Arial", 11, "bold")).pack(anchor="w")
        self.password = ttk.Entry(form, show="*", font=("Arial", 12)); self.password.pack(fill="x", pady=(4, 20))
        self.action_button(form, "Sign In", BLUE, self.login, width=250).pack(fill="x")
        tk.Label(form, text="Demo: admin / admin123", fg=MUTED, bg=LIGHT).pack(pady=14)
        self.username.focus()
        self.bind("<Return>", lambda event: self.login())

    def login(self):
        try:
            con = get_connection(); cur = con.cursor()
            cur.execute("SELECT full_name FROM users WHERE username=%s AND password=%s", (self.username.get().strip(), self.password.get()))
            user = cur.fetchone(); cur.close(); con.close()
            if user:
                self.show_dashboard(user[0])
            else:
                messagebox.showerror("Sign in failed", "Incorrect username or password.")
        except mysql.connector.Error as error:
            messagebox.showerror("Database error", f"Could not connect to MySQL.\n\n{error}\n\nCheck database.py and make sure MySQL is running.")

    def show_dashboard(self, full_name):
        self.unbind("<Return>")
        self.clear(); self.geometry("1100x650")
        header = tk.Frame(self, bg=NAVY, height=65); header.pack(fill="x"); header.pack_propagate(False)
        tk.Label(header, text="StudentHub", font=("Arial", 21, "bold"), fg="white", bg=NAVY).pack(side="left", padx=28, pady=17)
        self.action_button(header, "Logout", "#5B6F92", self.show_login).pack(side="right", padx=25, pady=15)
        tk.Label(header, text=f"Signed in as {full_name}", fg="#DCE6F8", bg=NAVY).pack(side="right")
        body = tk.Frame(self, bg=LIGHT, padx=28, pady=22); body.pack(fill="both", expand=True)
        top = tk.Frame(body, bg=LIGHT); top.pack(fill="x")
        tk.Label(top, text="Student Dashboard", font=("Arial", 23, "bold"), fg="#232D3D", bg=LIGHT).pack(side="left")
        self.total_label = tk.Label(top, text="Total Students: 0", font=("Arial", 12, "bold"), fg=BLUE, bg="white", padx=18, pady=12, relief="solid", bd=1)
        self.total_label.pack(side="right")
        tk.Label(body, text="Create, find and manage every student record.", fg=MUTED, bg=LIGHT).pack(anchor="w", pady=(2, 15))
        toolbar = tk.Frame(body, bg="white", padx=16, pady=14, relief="solid", bd=1); toolbar.pack(fill="x")
        tk.Label(toolbar, text="Search:", fg=TEXT, bg="white", font=("Arial", 11, "bold")).pack(side="left")
        self.search = ttk.Entry(toolbar, width=34); self.search.pack(side="left", padx=(8, 15)); self.search.bind("<KeyRelease>", lambda event: self.load_students())
        self.action_button(toolbar, "+ Add Student", BLUE, lambda: self.open_form()).pack(side="left", padx=4)
        self.action_button(toolbar, "Edit Selected", GREEN, self.edit_student).pack(side="left", padx=4)
        self.action_button(toolbar, "Delete Selected", RED, self.delete_student).pack(side="left", padx=4)
        table_frame = tk.Frame(body, bg="white", padx=10, pady=10, relief="solid", bd=1); table_frame.pack(fill="both", expand=True, pady=(12, 0))
        cols = ("id", "roll", "name", "email", "phone", "course", "age")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        headings = ("ID", "Roll No.", "Name", "Email", "Phone", "Course", "Age")
        widths = (45, 110, 160, 200, 125, 160, 60)
        for col, heading, width in zip(cols, headings, widths):
            self.tree.heading(col, text=heading); self.tree.column(col, width=width, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview); scroll.pack(side="right", fill="y"); self.tree.configure(yscrollcommand=scroll.set)
        self.load_students()

    @staticmethod
    def action_button(parent, text, color, command, width=None):
        # Labels are deliberately used as buttons: macOS native Tk buttons can ignore
        # foreground colours when the system appearance is dark.
        button = tk.Label(parent, text=text, bg=color, fg="white", cursor="hand2",
                          font=("Arial", 10, "bold"), padx=14, pady=9, width=width)
        button.bind("<Button-1>", lambda event: command())
        button.bind("<Enter>", lambda event: button.config(bg="#244FAD" if color == BLUE else color))
        button.bind("<Leave>", lambda event: button.config(bg=color))
        return button

    def load_students(self):
        try:
            text = self.search.get().strip() if hasattr(self, "search") else ""
            con = get_connection(); cur = con.cursor()
            term = f"%{text}%"
            cur.execute("SELECT id, roll_no, name, email, phone, course, age FROM students WHERE roll_no LIKE %s OR name LIKE %s OR course LIKE %s ORDER BY id DESC", (term, term, term))
            rows = cur.fetchall(); cur.execute("SELECT COUNT(*) FROM students"); total = cur.fetchone()[0]
            cur.close(); con.close()
            for item in self.tree.get_children(): self.tree.delete(item)
            for row in rows: self.tree.insert("", "end", values=row)
            self.total_label.config(text=f"Total Students: {total}")
        except mysql.connector.Error as error:
            messagebox.showerror("Database error", str(error))

    def selected_student(self):
        chosen = self.tree.selection()
        if not chosen:
            messagebox.showinfo("No selection", "Select a student row first.")
            return None
        return self.tree.item(chosen[0])["values"]

    def edit_student(self):
        student = self.selected_student()
        if student: self.open_form(student)

    def delete_student(self):
        student = self.selected_student()
        if not student or not messagebox.askyesno("Confirm delete", f"Delete {student[2]}?"): return
        try:
            con = get_connection(); cur = con.cursor(); cur.execute("DELETE FROM students WHERE id=%s", (student[0],)); con.commit(); cur.close(); con.close(); self.load_students()
        except mysql.connector.Error as error:
            messagebox.showerror("Could not delete", str(error))

    def open_form(self, student=None):
        win = tk.Toplevel(self); win.title("Add Student" if student is None else "Edit Student"); win.geometry("430x510"); win.resizable(False, False); win.transient(self); win.grab_set(); win.configure(bg=LIGHT)
        fields = ["Roll Number", "Name", "Email", "Phone", "Course", "Age"]
        values = ["", "", "", "", "", ""] if student is None else list(student[1:])
        entries = {}; form = tk.Frame(win, bg=LIGHT, padx=30, pady=25); form.pack(fill="both", expand=True)
        for label, value in zip(fields, values):
            tk.Label(form, text=label, fg=TEXT, bg=LIGHT, font=("Arial", 10, "bold")).pack(anchor="w", pady=(4, 1)); entry = ttk.Entry(form); entry.insert(0, str(value)); entry.pack(fill="x", pady=(0, 7)); entries[label] = entry
        def save():
            data = [entries[label].get().strip() for label in fields]
            if not data[0] or not data[1] or not data[4] or not data[5]:
                messagebox.showwarning("Missing details", "Fill Roll Number, Name, Course and Age.", parent=win); return
            try: age = int(data[5])
            except ValueError: messagebox.showwarning("Invalid age", "Age must be a number.", parent=win); return
            try:
                con = get_connection(); cur = con.cursor()
                if student is None:
                    cur.execute("INSERT INTO students (roll_no,name,email,phone,course,age) VALUES (%s,%s,%s,%s,%s,%s)", (*data[:5], age))
                else:
                    cur.execute("UPDATE students SET roll_no=%s,name=%s,email=%s,phone=%s,course=%s,age=%s WHERE id=%s", (*data[:5], age, student[0]))
                con.commit(); cur.close(); con.close(); win.destroy(); self.load_students()
            except mysql.connector.Error as error:
                messagebox.showerror("Could not save", str(error), parent=win)
        button_text = "Add Student" if student is None else "Update Student"
        self.action_button(form, button_text, BLUE, save).pack(pady=(14, 0), anchor="e")


if __name__ == "__main__":
    StudentApp().mainloop()
