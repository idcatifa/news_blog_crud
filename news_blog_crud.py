import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class NewsBlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Blog Management System")
        self.root.geometry("1200x650")
        self.root.configure(bg="#f0f8ff")

        # ---------------- MySQL Connection ----------------
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",        # XAMPP default has no password
            database="newsblog",
            port=3306
        )
        self.cursor = self.db.cursor(dictionary=True)

        # ---------------- GUI ----------------
        self.create_gui()
        self.load_users()
        self.load_news()

    # ---------------- GUI Elements ----------------
    def create_gui(self):
        # Header
        header = tk.Label(self.root, text="News Blog Management System", font=("Helvetica", 24, "bold"),
                          bg="#007acc", fg="white", pady=15)
        header.pack(fill="x")

        # Search
        search_frame = tk.Frame(self.root, bg="#f0f8ff")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", font=("Helvetica", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12))
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search).pack(side="left")

        # Users Frame
        frame_users = tk.LabelFrame(self.root, text="Users", font=("Helvetica", 14, "bold"), bg="#f0f8ff",
                                    padx=10, pady=10)
        frame_users.place(x=20, y=100, width=550, height=500)

        self.user_tree = ttk.Treeview(frame_users, columns=("ID", "Username", "Email", "Age", "Contact"), show="headings", height=20)
        for col, w in zip(["ID", "Username", "Email", "Age", "Contact"], [50, 150, 150, 50, 100]):
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=w)
        self.user_tree.pack(fill="both", expand=True)

        # Bind user selection
        self.user_tree.bind("<ButtonRelease-1>", self.on_user_select)

        # News Frame
        frame_news = tk.LabelFrame(self.root, text="News", font=("Helvetica", 14, "bold"), bg="#f0f8ff", padx=10, pady=10)
        frame_news.place(x=600, y=100, width=580, height=500)

        self.news_tree = ttk.Treeview(frame_news, columns=("ID", "Username", "Title", "Body", "Created At"), show="headings", height=20)
        for col, w in zip(["ID", "Username", "Title", "Body", "Created At"], [50, 100, 150, 200, 120]):
            self.news_tree.heading(col, text=col)
            self.news_tree.column(col, width=w)
        self.news_tree.pack(fill="both", expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f8ff")
        btn_frame.place(x=20, y=610, width=1160, height=40)

        tk.Button(btn_frame, text="Load Users", command=self.load_users, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Add User", command=self.add_user, width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Update User", command=self.update_user, width=15).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Delete User", command=self.delete_user, width=15).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Load News", command=self.load_news, width=15).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Add News", command=self.add_news, width=15).grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Update News", command=self.update_news, width=15).grid(row=0, column=6, padx=5)
        tk.Button(btn_frame, text="Delete News", command=self.delete_news, width=15).grid(row=0, column=7, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.close, width=15).grid(row=0, column=8, padx=5)

    # ---------------- CRUD Functions ----------------
    def load_users(self, search=""):
        query = "SELECT * FROM user"
        if search:
            query += f" WHERE username LIKE '%{search}%' OR email LIKE '%{search}%'"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for u in users:
            self.user_tree.insert("", "end", values=(u['user_id'], u['username'], u['email'], u['age'], u['contact_number']))

    def load_news(self, search="", user_id=None):
        query = """
            SELECT n.news_id, u.username, n.title, n.body, n.created_at
            FROM news n
            JOIN user u ON n.user_id = u.user_id
        """
        conditions = []
        if user_id:
            conditions.append(f"n.user_id={user_id}")
        if search:
            conditions.append(f"(n.title LIKE '%{search}%' OR n.body LIKE '%{search}%')")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY n.news_id"
        self.cursor.execute(query)
        news = self.cursor.fetchall()
        for row in self.news_tree.get_children():
            self.news_tree.delete(row)
        for n in news:
            self.news_tree.insert("", "end", values=(n['news_id'], n['username'], n['title'], n['body'], n['created_at']))

    # ---------------- Add User ----------------
    def add_user(self):
        win = tk.Toplevel(self.root)
        win.title("Add User")
        win.geometry("300x250")
        win.grab_set()

        tk.Label(win, text="Username:").pack(pady=5)
        username_entry = tk.Entry(win)
        username_entry.pack(pady=5)

        tk.Label(win, text="Email:").pack(pady=5)
        email_entry = tk.Entry(win)
        email_entry.pack(pady=5)

        tk.Label(win, text="Age:").pack(pady=5)
        age_entry = tk.Entry(win)
        age_entry.pack(pady=5)

        tk.Label(win, text="Contact Number:").pack(pady=5)
        contact_entry = tk.Entry(win)
        contact_entry.pack(pady=5)

        def submit():
            username = username_entry.get()
            email = email_entry.get()
            age = age_entry.get()
            contact = contact_entry.get()
            if not username or not email or not age or not contact:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            try:
                age = int(age)
            except ValueError:
                messagebox.showwarning("Input Error", "Age must be a number")
                return
            self.cursor.execute(
                "INSERT INTO user (username,email,age,contact_number) VALUES (%s,%s,%s,%s)",
                (username, email, age, contact)
            )
            self.db.commit()
            messagebox.showinfo("Success", "User added successfully")
            win.destroy()
            self.load_users()

        username_entry.bind("<Return>", lambda e: email_entry.focus())
        email_entry.bind("<Return>", lambda e: age_entry.focus())
        age_entry.bind("<Return>", lambda e: contact_entry.focus())
        contact_entry.bind("<Return>", lambda e: submit())

        username_entry.focus()

    # ---------------- Update User ----------------
    def update_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Select User", "Select a user to update")
            return
        user_id, uname, email, age, contact = self.user_tree.item(selected[0])['values']

        win = tk.Toplevel(self.root)
        win.title("Update User")
        win.geometry("300x250")
        win.grab_set()

        tk.Label(win, text="Username:").pack(pady=5)
        username_entry = tk.Entry(win)
        username_entry.insert(0, uname)
        username_entry.pack(pady=5)

        tk.Label(win, text="Email:").pack(pady=5)
        email_entry = tk.Entry(win)
        email_entry.insert(0, email)
        email_entry.pack(pady=5)

        tk.Label(win, text="Age:").pack(pady=5)
        age_entry = tk.Entry(win)
        age_entry.insert(0, age)
        age_entry.pack(pady=5)

        tk.Label(win, text="Contact Number:").pack(pady=5)
        contact_entry = tk.Entry(win)
        contact_entry.insert(0, contact)
        contact_entry.pack(pady=5)

        def submit():
            new_uname = username_entry.get()
            new_email = email_entry.get()
            new_age = age_entry.get()
            new_contact = contact_entry.get()
            if not new_uname or not new_email or not new_age or not new_contact:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            try:
                new_age = int(new_age)
            except ValueError:
                messagebox.showwarning("Input Error", "Age must be a number")
                return
            self.cursor.execute(
                "UPDATE user SET username=%s,email=%s,age=%s,contact_number=%s WHERE user_id=%s",
                (new_uname, new_email, new_age, new_contact, user_id)
            )
            self.db.commit()
            messagebox.showinfo("Success", "User updated successfully")
            win.destroy()
            self.load_users()
            self.load_news()

        username_entry.bind("<Return>", lambda e: email_entry.focus())
        email_entry.bind("<Return>", lambda e: age_entry.focus())
        age_entry.bind("<Return>", lambda e: contact_entry.focus())
        contact_entry.bind("<Return>", lambda e: submit())

        username_entry.focus()

    # ---------------- Delete User ----------------
    def delete_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Select User", "Select a user to delete")
            return
        user_id = self.user_tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", "Delete this user and all their news?")
        if confirm:
            self.cursor.execute("DELETE FROM user WHERE user_id=%s", (user_id,))
            self.db.commit()
            messagebox.showinfo("Deleted", "User deleted successfully")
            self.load_users()
            self.load_news()

    # ---------------- Add News (auto user selection) ----------------
    def add_news(self):
        selected_user = self.user_tree.selection()
        if not selected_user:
            messagebox.showwarning("Select User", "Please select a user first")
            return

        user_id = self.user_tree.item(selected_user[0])['values'][0]
        username = self.user_tree.item(selected_user[0])['values'][1]

        win = tk.Toplevel(self.root)
        win.title(f"Add News for {username}")
        win.geometry("300x200")
        win.grab_set()

        tk.Label(win, text="Title:").pack(pady=5)
        title_entry = tk.Entry(win)
        title_entry.pack(pady=5)

        tk.Label(win, text="Body:").pack(pady=5)
        body_entry = tk.Entry(win)
        body_entry.pack(pady=5)

        def submit():
            title = title_entry.get()
            body = body_entry.get()
            if not title or not body:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            self.cursor.execute(
                "INSERT INTO news (user_id,title,body) VALUES (%s,%s,%s)",
                (user_id, title, body)
            )
            self.db.commit()
            messagebox.showinfo("Success", "News added successfully")
            win.destroy()
            self.load_news(user_id=user_id)

        title_entry.bind("<Return>", lambda e: body_entry.focus())
        body_entry.bind("<Return>", lambda e: submit())

        title_entry.focus()

    # ---------------- Update News ----------------
    def update_news(self):
        selected = self.news_tree.selection()
        if not selected:
            messagebox.showwarning("Select News", "Select news to update")
            return
        news_id, uname, title, body, created = self.news_tree.item(selected[0])['values']

        win = tk.Toplevel(self.root)
        win.title("Update News")
        win.geometry("300x200")
        win.grab_set()

        tk.Label(win, text="Title:").pack(pady=5)
        title_entry = tk.Entry(win)
        title_entry.insert(0, title)
        title_entry.pack(pady=5)

        tk.Label(win, text="Body:").pack(pady=5)
        body_entry = tk.Entry(win)
        body_entry.insert(0, body)
        body_entry.pack(pady=5)

        def submit():
            new_title = title_entry.get()
            new_body = body_entry.get()
            if not new_title or not new_body:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            self.cursor.execute("UPDATE news SET title=%s,body=%s WHERE news_id=%s", (new_title, new_body, news_id))
            self.db.commit()
            messagebox.showinfo("Success", "News updated successfully")
            win.destroy()
            self.load_news()

        title_entry.bind("<Return>", lambda e: body_entry.focus())
        body_entry.bind("<Return>", lambda e: submit())

        title_entry.focus()

    # ---------------- Delete News ----------------
    def delete_news(self):
        selected = self.news_tree.selection()
        if not selected:
            messagebox.showwarning("Select News", "Select news to delete")
            return
        news_id = self.news_tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", "Delete this news?")
        if confirm:
            self.cursor.execute("DELETE FROM news WHERE news_id=%s", (news_id,))
            self.db.commit()
            messagebox.showinfo("Deleted", "News deleted successfully")
            self.load_news()

    # ---------------- User selection ----------------
    def on_user_select(self, event):
        selected = self.user_tree.selection()
        if selected:
            user_id = self.user_tree.item(selected[0])['values'][0]
            self.load_news(user_id=user_id)

    # ---------------- Search ----------------
    def search(self):
        term = self.search_entry.get()
        self.load_users(term)
        self.load_news(term)

    # ---------------- Close ----------------
    def close(self):
        self.cursor.close()
        self.db.close()
        self.root.destroy()

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NewsBlogApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
