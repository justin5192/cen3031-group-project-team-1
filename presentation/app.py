#ui_app.py
import tkinter as tk
from tkinter import messagebox
from core_logic.data_persistence import DataPersistence # Assuming this path is correct
from core_logic.calculator import CarbonFootprintCalculator # This is the correct import
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib # For securely identifying users in the UI, though data_persistence handles the hashing

# --- Data Schemas and Constants ---
ACTIVITY_CATEGORIES = [
    "Transportation (Car, Bus, Train, Plane)",
    "Electricity Usage",
    "Food Consumption",
    "Waste Generation"
]

# --- Main Application Class ---

class CarbonTrackerApp(tk.Tk):
    """The main application window and controller."""
    def __init__(self):
        super().__init__()
        self.title("CarbonTracker")
        self.geometry("800x600")
        
        # Initialize Core Services
        self.data_persistence = DataPersistence()
        self.carbon_calculator = CarbonFootprintCalculator()
        
        # State Variables
        self.current_user = None
        
        # UI Elements
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.create_pages()
        self.show_frame("LoginPage")

    def create_pages(self):
        """Creates and stores all main application pages."""
        for F in (LoginPage, DashboardPage, LogActivityPage, GoalsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Raises the requested frame to the top."""
        frame = self.frames[page_name]
        frame.tkraise()
        # Refresh data when navigating to the Dashboard
        if page_name == "DashboardPage":
            frame.refresh_data()
            
    def set_user(self, username):
        """Sets the current user and navigates to the dashboard."""
        self.current_user = username
        self.show_frame("DashboardPage")
        
    def logout(self):
        """Logs out the current user and returns to the login page."""
        self.current_user = None
        self.frames["LoginPage"].reset_fields()
        self.show_frame("LoginPage")

# --- Login Page ---

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padx=20, pady=20)
        
        # Center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Title
        tk.Label(self, text="CarbonTracker Login", font=("Arial", 24, "bold")).grid(row=0, column=1, pady=(0, 40))

        # Username
        tk.Label(self, text="Username:", font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=(10, 0))
        self.username_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.username_entry.grid(row=2, column=1, pady=(0, 10), ipady=5, sticky="ew")

        # Password
        tk.Label(self, text="Password:", font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=(10, 0))
        self.password_entry = tk.Entry(self, width=30, show="*", font=("Arial", 12))
        self.password_entry.grid(row=4, column=1, pady=(0, 20), ipady=5, sticky="ew")

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=1, pady=20)

        # Login Button
        tk.Button(button_frame, text="Login", command=self.handle_login, width=15, height=2, font=("Arial", 12)).pack(pady=5)

        # Register Button
        tk.Button(button_frame, text="Register", command=self.handle_register, width=15, height=2, font=("Arial", 12)).pack(pady=5)
        
    def reset_fields(self):
        """Clears the username and password fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def handle_login(self):
        """Handles user login attempt."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password.")
            return

        success, message = self.controller.data_persistence.authenticate_user(username, password)

        if success:
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.controller.set_user(username)
        else:
            messagebox.showerror("Login Failed", message)

    def handle_register(self):
        """
        Handles user registration attempt.
        
        CRUCIAL: This method has been updated to correctly check the boolean success 
        flag and display the specific error message returned by register_user().
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty.")
            return
            
        # Call the updated register_user which returns (success_bool, message_string)
        success, message = self.controller.data_persistence.register_user(username, password)
        
        if success:
            messagebox.showinfo("Registration Successful", "You are now registered! Please log in.")
            # Clear fields but stay on the page
            self.reset_fields()
        else:
            # Display the specific error message, including file permission errors
            messagebox.showerror("Registration Failed", message)

# --- Dashboard Page ---

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padx=20, pady=20)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Top Frame for Header and Navigation
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        # Title
        tk.Label(top_frame, text="Carbon Dashboard", font=("Arial", 20, "bold")).grid(row=0, column=1, sticky="n")

        # Navigation Buttons
        tk.Button(top_frame, text="Log Activity", command=lambda: controller.show_frame("LogActivityPage")).grid(row=0, column=0, sticky="w")
        tk.Button(top_frame, text="Set Goal", command=lambda: controller.show_frame("GoalsPage")).grid(row=0, column=2, sticky="e")
        
        # Logout Button
        tk.Button(top_frame, text="Logout", command=controller.logout).grid(row=1, column=2, sticky="e")

        # --- Main Content Frame ---
        main_content_frame = tk.Frame(self)
        main_content_frame.grid(row=1, column=0, sticky="nsew")
        main_content_frame.grid_columnconfigure(0, weight=1)
        main_content_frame.grid_columnconfigure(1, weight=1)
        main_content_frame.grid_rowconfigure(0, weight=1)

        # Left Panel: Summary/Goal Progress
        left_panel = tk.Frame(main_content_frame, bd=2, relief="groove")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        
        tk.Label(left_panel, text="Weekly Summary", font=("Arial", 16, "underline")).pack(pady=10)
        
        self.total_footprint_label = tk.Label(left_panel, text="Total Footprint (Last 7 Days): N/A", font=("Arial", 12))
        self.total_footprint_label.pack(pady=5)
        
        self.goal_label = tk.Label(left_panel, text="Weekly Goal: N/A", font=("Arial", 12))
        self.goal_label.pack(pady=5)

        self.progress_bar_value = tk.DoubleVar()
        self.progress_bar = tk.Label(left_panel, textvariable=self.progress_bar_value, width=20, bg='lightgray')
        self.progress_bar.pack(pady=10, fill='x', padx=10)
        
        # Activity breakdown graph placeholder
        self.graph_frame = tk.Frame(left_panel)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.chart = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.chart_widget = self.chart.get_tk_widget()
        self.chart_widget.pack(fill="both", expand=True)

        # Right Panel: Recent Activity Log
        right_panel = tk.Frame(main_content_frame, bd=2, relief="groove")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)

        tk.Label(right_panel, text="Recent Activity Log", font=("Arial", 16, "underline")).pack(pady=10)

        self.log_listbox = tk.Listbox(right_panel, font=("Arial", 10), height=15)
        self.log_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Edit/Delete buttons
        log_button_frame = tk.Frame(right_panel)
        log_button_frame.pack(pady=10)
        tk.Button(log_button_frame, text="Edit Selected", command=self.edit_selected_log).pack(side="left", padx=5)
        tk.Button(log_button_frame, text="Delete Selected", command=self.delete_selected_log).pack(side="left", padx=5)

    def calculate_weekly_footprint(self, logs):
        """Calculates total footprint for the last 7 days."""
        seven_days_ago = datetime.now() - datetime.timedelta(days=7)
        weekly_footprint = 0.0
        
        # Calculate breakdown for the pie chart
        breakdown = {cat: 0.0 for cat in ACTIVITY_CATEGORIES}

        for log in logs:
            try:
                log_dt = datetime.fromisoformat(log.get('timestamp'))
                footprint = log.get('footprint', 0.0)
                category = log.get('category', 'Unknown')
                
                if log_dt >= seven_days_ago:
                    weekly_footprint += footprint
                
                # For the chart, we use all logs or just the weekly? Let's use all for breakdown.
                # If you want weekly breakdown, you'd apply the same date filter here.
                if category in breakdown:
                    breakdown[category] += footprint
                
            except:
                # Skip logs with bad formatting
                continue
                
        return weekly_footprint, breakdown

    def refresh_data(self):
        """Fetches and displays the latest user data."""
        if not self.controller.current_user:
            return

        username = self.controller.current_user
        
        # 1. Load Data
        user_data = self.controller.data_persistence.load_user_data(username)
        logs = user_data.get('logs', [])
        current_goal = user_data.get('goal', 100.0)
        
        # 2. Calculate Footprint
        weekly_footprint, breakdown = self.calculate_weekly_footprint(logs)
        
        # 3. Update Summary Labels
        self.total_footprint_label.config(text=f"Total Footprint (Last 7 Days): {weekly_footprint:.2f} kg CO2")
        self.goal_label.config(text=f"Weekly Goal: {current_goal:.2f} kg CO2")
        
        # 4. Update Progress Bar
        progress = min(weekly_footprint / current_goal, 1.0) * 100
        self.progress_bar_value.set(f"Progress: {progress:.1f}%")
        
        # Update progress bar background color to visually represent progress
        bar_width = int(self.progress_bar['width'] * (progress / 100))
        if progress < 70:
            color = 'green'
        elif progress < 100:
            color = 'yellow'
        else:
            color = 'red'

        # This simple text-based progress bar is a placeholder for a proper Tkinter-progress-bar
        self.progress_bar.config(bg=color)


        # 5. Update Activity Log
        self.log_listbox.delete(0, tk.END)
        # Reverse to show most recent first
        for i, log in enumerate(reversed(logs)):
            display_text = f"[{i+1}] {log.get('timestamp', 'No Date')[:10]} - {log.get('category', 'N/A')}: {log.get('footprint', 0.0):.2f} kg CO2"
            self.log_listbox.insert(tk.END, display_text)
            
        # 6. Update Pie Chart
        self.update_pie_chart(breakdown)

    def update_pie_chart(self, breakdown):
        """Generates and updates the Matplotlib pie chart."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Filter out zero values for better chart display
        labels = [k for k, v in breakdown.items() if v > 0]
        sizes = [v for v in breakdown.values() if v > 0]

        if sizes:
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title("Carbon Footprint Breakdown")
        else:
            ax.text(0.5, 0.5, "No activity logs yet.", ha='center', va='center')
        
        self.chart.draw()
        
    def edit_selected_log(self):
        """Opens the LogActivityPage to edit the selected log entry."""
        selection = self.log_listbox.curselection()
        if not selection:
            messagebox.showinfo("Edit Log", "Please select an activity log to edit.")
            return

        # The listbox is reversed, so we need to calculate the true index
        logs = self.controller.data_persistence.get_all_activity_logs(self.controller.current_user)
        list_index = selection[0]
        true_index = len(logs) - 1 - list_index # Index of the log in the original list
        
        if 0 <= true_index < len(logs):
            log_data = logs[true_index]
            # Navigate to LogActivityPage and pass the log data and index for editing
            log_page = self.controller.frames["LogActivityPage"]
            log_page.load_for_edit(true_index, log_data)
            self.controller.show_frame("LogActivityPage")

    def delete_selected_log(self):
        """Deletes the selected log entry."""
        selection = self.log_listbox.curselection()
        if not selection:
            messagebox.showinfo("Delete Log", "Please select an activity log to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this activity log?"):
            logs = self.controller.data_persistence.get_all_activity_logs(self.controller.current_user)
            list_index = selection[0]
            true_index = len(logs) - 1 - list_index # Index of the log in the original list
            
            if self.controller.data_persistence.delete_activity_log(self.controller.current_user, true_index):
                messagebox.showinfo("Success", "Activity log deleted.")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to delete activity log.")


# --- Log Activity Page ---

class LogActivityPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padx=20, pady=20)
        self.editing_index = None # Stores the index of the log being edited
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        tk.Label(self, text="Log Carbon Activity", font=("Arial", 24, "bold")).grid(row=0, column=1, pady=(0, 40))

        # Input Fields
        self.category_var = tk.StringVar(self)
        self.category_var.set(ACTIVITY_CATEGORIES[0]) # default value

        tk.Label(self, text="Category:", font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=(10, 0))
        self.category_menu = tk.OptionMenu(self, self.category_var, *ACTIVITY_CATEGORIES)
        self.category_menu.config(font=("Arial", 12), width=30)
        self.category_menu.grid(row=2, column=1, pady=(0, 10), ipady=5, sticky="ew")

        tk.Label(self, text="Activity Description:", font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=(10, 0))
        self.description_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.description_entry.grid(row=4, column=1, pady=(0, 10), ipady=5, sticky="ew")

        tk.Label(self, text="Footprint (kg CO2e):", font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=(10, 0))
        self.footprint_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.footprint_entry.grid(row=6, column=1, pady=(0, 20), ipady=5, sticky="ew")

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=7, column=1, pady=20)

        self.submit_button = tk.Button(button_frame, text="Submit Log", command=self.handle_submit, width=15, height=2, font=("Arial", 12))
        self.submit_button.pack(side="left", padx=10)

        tk.Button(button_frame, text="Back to Dashboard", command=self.go_back, width=15, height=2, font=("Arial", 12)).pack(side="left", padx=10)
        
    def reset_fields(self):
        """Clears fields and resets to default 'add' mode."""
        self.category_var.set(ACTIVITY_CATEGORIES[0])
        self.description_entry.delete(0, tk.END)
        self.footprint_entry.delete(0, tk.END)
        self.editing_index = None
        self.submit_button.config(text="Submit Log")
        
    def load_for_edit(self, index, log_data):
        """Loads log data into fields for editing."""
        self.editing_index = index
        self.category_var.set(log_data.get('category', ACTIVITY_CATEGORIES[0]))
        
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, log_data.get('description', ''))
        
        self.footprint_entry.delete(0, tk.END)
        self.footprint_entry.insert(0, str(log_data.get('footprint', 0.0)))
        
        self.submit_button.config(text="Update Log")

    def handle_submit(self):
        """Handles submission (add or update) of the activity log."""
        try:
            footprint = float(self.footprint_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Footprint must be a valid number.")
            return

        log_data = {
            "category": self.category_var.get(),
            "description": self.description_entry.get(),
            "footprint": footprint,
            # Timestamp is added/preserved by the data persistence layer
        }
        
        user = self.controller.current_user

        if self.editing_index is not None:
            # Update existing log
            success = self.controller.data_persistence.update_activity_log(user, self.editing_index, log_data)
            if success:
                messagebox.showinfo("Success", "Activity log updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update activity log.")
        else:
            # Add new log
            self.controller.data_persistence.add_activity_log(user, log_data)
            messagebox.showinfo("Success", "Activity log submitted successfully.")

        self.go_back()

    def go_back(self):
        """Resets fields and returns to the dashboard."""
        self.reset_fields()
        self.controller.show_frame("DashboardPage")

# --- Goals Page ---

class GoalsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padx=20, pady=20)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        tk.Label(self, text="Set Weekly Carbon Goal", font=("Arial", 24, "bold")).grid(row=0, column=1, pady=(0, 40))

        # Current Goal Display
        self.current_goal_var = tk.StringVar(self)
        tk.Label(self, textvariable=self.current_goal_var, font=("Arial", 14)).grid(row=1, column=1, pady=10)
        
        tk.Label(self, text="New Weekly Goal (kg CO2e):", font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.goal_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.goal_entry.grid(row=3, column=1, pady=(0, 20), ipady=5, sticky="ew")

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=1, pady=20)

        tk.Button(button_frame, text="Set Goal", command=self.handle_set_goal, width=15, height=2, font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back to Dashboard", command=self.go_back, width=15, height=2, font=("Arial", 12)).pack(side="left", padx=10)
        
        # Initial load when the page is first created
        self.bind("<Visibility>", self.load_current_goal)

    def load_current_goal(self, event=None):
        """Loads and displays the current goal when the page becomes visible."""
        if self.controller.current_user:
            user_data = self.controller.data_persistence.load_user_data(self.controller.current_user)
            current_goal = user_data.get('goal', 100.0)
            self.current_goal_var.set(f"Current Goal: {current_goal:.2f} kg CO2e")
            self.goal_entry.delete(0, tk.END)
            self.goal_entry.insert(0, str(current_goal))

    def handle_set_goal(self):
        """Handles the setting of a new weekly carbon goal."""
        try:
            new_goal = float(self.goal_entry.get())
            if new_goal <= 0:
                raise ValueError("Goal must be a positive number.")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid goal value: {e}")
            return

        user = self.controller.current_user
        if not user:
            messagebox.showerror("Error", "No user logged in.")
            return

        user_data = self.controller.data_persistence.load_user_data(user)
        user_data['goal'] = new_goal
        
        try:
            self.controller.data_persistence.save_user_data(user, user_data)
            messagebox.showinfo("Success", f"Weekly goal set to {new_goal:.2f} kg CO2e.")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save new goal: {e}")
            
    def go_back(self):
        """Returns to the dashboard."""
        self.controller.show_frame("DashboardPage")

# --- Main Run Block ---

def run_app():
    """Initializes and runs the application."""
    app = CarbonTrackerApp()
    app.mainloop()

if __name__ == '__main__':
    run_app()
