import tkinter as tk
from tkinter import ttk, messagebox
from auth import login_user, register_user, init_excel_db
from styles import configure_styles
from excel_db import init_excel_db
from teacher_ui import TeacherDashboard
from student_ui import StudentDashboard

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # initialization
        init_excel_db()
        
        # Basic Setup
        self.title("Quiz Application - Login")
        self.geometry("500x400")
        self.resizable(False, False)
        configure_styles(self)
        
        # Track active windows
        self.active_dashboard = None
        
        # UI Create
        self._setup_ui()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_ui(self):
        bg_frame = ttk.Frame(self)
        bg_frame.pack(fill='both', expand=True)

        self.main_frame = ttk.Frame(bg_frame)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Username
        ttk.Label(self.main_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.userid_entry = ttk.Entry(self.main_frame)
        self.userid_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        ttk.Label(self.main_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(self.main_frame, text="Login", command=self.login).grid(row=2, column=1, pady=10)
        ttk.Button(self.main_frame, text="Register", command=self.show_register).grid(row=3, column=1, pady=10)

        # Copyright text at the bottom
        copyright_label = ttk.Label(bg_frame, text="© 2025 Quiz Application. All rights reserved.", font=('Helvetica', 8))
        copyright_label.pack(side='bottom', pady=10)

    def login(self):
        username = self.userid_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password required")
            return
        
        user_data = login_user(username, password)
        
        if user_data:
            if user_data['role'] == 'teacher':
                self.active_dashboard = TeacherDashboard(self, user_data['id'], user_data['name'])
            else:
                self.active_dashboard = StudentDashboard(self, user_data['id'], user_data['name'])
            
            self.active_dashboard.protocol("WM_DELETE_WINDOW", lambda: self._on_dashboard_close(self.active_dashboard))
            self.withdraw()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def _on_dashboard_close(self, dashboard_window):
        """Handle dashboard window close"""
        if messagebox.askokcancel("Logout", "Do you want to logout?"):
            dashboard_window.destroy()
            self.active_dashboard = None
            self.deiconify()
            # Clear login fields
            self.userid_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def show_register(self):
        self.register_window = tk.Toplevel(self)
        self.register_window.title("Register")
        self.register_window.geometry("400x300")
        self.register_window.resizable(False, False) # Disable window resizing
        self.register_window.transient(self)
        
        # Center the window relative to the main window
        x = self.winfo_x() + (self.winfo_width() - 400) // 2
        y = self.winfo_y() + (self.winfo_height() - 300) // 2
        self.register_window.geometry(f"+{x}+{y}")

        # Create background frame
        bg_frame = ttk.Frame(self.register_window)
        bg_frame.pack(fill='both', expand=True)

        # Create main frame for centered content
        main_frame = ttk.Frame(bg_frame)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        title_label = ttk.Label(main_frame, text="Create New Account", font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.reg_username = ttk.Entry(main_frame, width=25)
        self.reg_username.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.reg_password = ttk.Entry(main_frame, show="*", width=25)
        self.reg_password.grid(row=2, column=1, padx=5, pady=5)
        
        # Role
        ttk.Label(main_frame, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.reg_role = ttk.Combobox(main_frame, values=["student", "teacher"], state="readonly", width=23)
        self.reg_role.grid(row=3, column=1, padx=5, pady=5)
        self.reg_role.current(0)  
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Register button
        register_btn = ttk.Button(button_frame, text="Register", command=self.register_user, width=15)
        register_btn.pack(side='left', padx=5)
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.register_window.destroy, width=15)
        cancel_btn.pack(side='left', padx=5)

        # Handle window close
        self.register_window.protocol("WM_DELETE_WINDOW", self.register_window.destroy)
        
        # Set focus to username field
        self.reg_username.focus()
        
        # Bind Enter key to register
        self.register_window.bind('<Return>', lambda e: self.register_user())

    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        role = self.reg_role.get()
        
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if register_user(username, password, role):
            messagebox.showinfo("Success", "Registration successful!")
            self.register_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists")

    def on_closing(self):
        """Handle main window close"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            if self.active_dashboard:
                self.active_dashboard.destroy()
            self.quit()

if __name__ == "__main__":
    init_excel_db()  
    app = LoginApp()
    app.mainloop()
