# ui/app.py
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core_logic.data_persistence import DataPersistence
from core_logic.calculator import CarbonFootprintCalculator
from core_logic.constants import MAIN_CATEGORIES, DEFAULT_WEEKLY_GOAL
from core_logic.tips import get_contextual_tip, get_random_tip

# --- Main Application Class ---

class CarbonTrackerApp(tk.Tk):
    """The main application window and controller."""
    def __init__(self):
        super().__init__()
        self.title("CarbonTracker")
        
        # Set window size - optimized for complete pie chart display
        window_width = 1100
        window_height = 1100  # Increased to 950 for optimal pie chart display
        
        # Center the window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.minsize(1000, 700)
        
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
        for F in (LoginPage, DashboardPage, LogActivityPage, GoalsPage, TimelineGraphPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Raises the requested frame to the top."""
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Refresh data when navigating to specific pages
        if page_name == "DashboardPage":
            frame.refresh_data()
        elif page_name == "TimelineGraphPage":
            frame.refresh_graph()
        elif page_name == "GoalsPage":
            frame.load_current_goal()
            
    def set_user(self, username):
        """Sets the current user and navigates appropriately."""
        self.current_user = username
        
        # Check if user needs initial goal setting
        if self.data_persistence.needs_initial_goal_setting(username):
            messagebox.showinfo("Welcome!", "Let's set up your carbon reduction goal!")
            self.show_frame("GoalsPage")
        else:
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
            self.controller.set_user(username)
        else:
            messagebox.showerror("Login Failed", message)

    def handle_register(self):
        """Handles user registration attempt."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty.")
            return
            
        success, message = self.controller.data_persistence.register_user(username, password)
        
        if success:
            messagebox.showinfo("Registration Successful", "Account created! Setting up your profile...")
            self.reset_fields()
            # Auto-login and redirect to goal setting
            self.controller.set_user(username)
        else:
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
        nav_left = tk.Frame(top_frame)
        nav_left.grid(row=0, column=0, sticky="w")
        tk.Button(nav_left, text="Log Activity", command=lambda: controller.show_frame("LogActivityPage")).pack(side="left", padx=5)
        tk.Button(nav_left, text="Set Goal", command=lambda: controller.show_frame("GoalsPage")).pack(side="left", padx=5)
        tk.Button(nav_left, text="Timeline Graph", command=lambda: controller.show_frame("TimelineGraphPage")).pack(side="left", padx=5)
        
        # Logout and Export buttons
        nav_right = tk.Frame(top_frame)
        nav_right.grid(row=0, column=2, sticky="e")
        tk.Button(nav_right, text="Export Data", command=self.export_data).pack(side="left", padx=5)
        tk.Button(nav_right, text="Logout", command=controller.logout).pack(side="left", padx=5)

        # --- Main Content Frame ---
        main_content_frame = tk.Frame(self)
        main_content_frame.grid(row=1, column=0, sticky="nsew")
        main_content_frame.grid_columnconfigure(0, weight=2)  # Left panel gets more weight
        main_content_frame.grid_columnconfigure(1, weight=3)  # Right panel gets more weight
        main_content_frame.grid_rowconfigure(0, weight=1)

        # Left Panel: Summary/Goal Progress
        left_panel = tk.Frame(main_content_frame, bd=2, relief="groove")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_panel.grid_columnconfigure(0, weight=1)
        
        tk.Label(left_panel, text="Weekly Summary", font=("Arial", 16, "underline")).pack(pady=10)
        
        self.total_footprint_label = tk.Label(left_panel, text="Total Footprint (Last 7 Days): N/A", font=("Arial", 12))
        self.total_footprint_label.pack(pady=5)
        
        self.goal_label = tk.Label(left_panel, text="Weekly Goal: N/A", font=("Arial", 12))
        self.goal_label.pack(pady=5)

        # Progress bar
        self.progress_label = tk.Label(left_panel, text="Progress: 0%", font=("Arial", 11))
        self.progress_label.pack(pady=5)
        
        self.progress_canvas = tk.Canvas(left_panel, height=30, bg='lightgray')
        self.progress_canvas.pack(fill='x', padx=10, pady=5)
        
        # Comparison to average
        tk.Label(left_panel, text="Comparison", font=("Arial", 14, "underline")).pack(pady=(20, 10))
        self.comparison_label = tk.Label(left_panel, text="Loading...", font=("Arial", 11), wraplength=300, justify="left")
        self.comparison_label.pack(pady=5)
        
        # Reduction tip
        tk.Label(left_panel, text="💡 Tip of the Day", font=("Arial", 14, "underline")).pack(pady=(20, 10))
        self.tip_label = tk.Label(left_panel, text="Loading...", font=("Arial", 10), wraplength=300, justify="left", fg="darkgreen")
        self.tip_label.pack(pady=5, padx=10)
        
        # Activity breakdown graph
        tk.Label(left_panel, text="Category Breakdown", font=("Arial", 14, "underline")).pack(pady=(15, 5))
        self.graph_frame = tk.Frame(left_panel)
        self.graph_frame.pack(fill="both", expand=True, padx=5, pady=(5, 15))
        self.fig = plt.Figure(figsize=(7, 6), dpi=75)  # Much larger figure
        self.chart = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.chart_widget = self.chart.get_tk_widget()
        self.chart_widget.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Initial empty chart
        # Don't draw immediately - wait for window to render
        self.bind("<Map>", self._on_first_show)

        # Right Panel: Recent Activity Log
        right_panel = tk.Frame(main_content_frame, bd=2, relief="groove")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_panel.grid_columnconfigure(0, weight=1)

        tk.Label(right_panel, text="Recent Activity Log", font=("Arial", 16, "underline")).pack(pady=10)

        # Filter and sort controls
        controls_frame = tk.Frame(right_panel)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(controls_frame, text="Filter:").pack(side="left", padx=5)
        self.filter_var = tk.StringVar(value="All")
        filter_options = ["All"] + list(MAIN_CATEGORIES.keys())
        self.filter_dropdown = ttk.Combobox(controls_frame, textvariable=self.filter_var, values=filter_options, state="readonly", width=15)
        self.filter_dropdown.pack(side="left", padx=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        tk.Label(controls_frame, text="Sort:").pack(side="left", padx=5)
        self.sort_var = tk.StringVar(value="Date (Newest)")
        sort_options = ["Date (Newest)", "Date (Oldest)", "Footprint (High-Low)", "Footprint (Low-High)"]
        self.sort_dropdown = ttk.Combobox(controls_frame, textvariable=self.sort_var, values=sort_options, state="readonly", width=18)
        self.sort_dropdown.pack(side="left", padx=5)
        self.sort_dropdown.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        self.log_listbox = tk.Listbox(right_panel, font=("Arial", 10), height=25)
        self.log_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Edit/Delete buttons
        log_button_frame = tk.Frame(right_panel)
        log_button_frame.pack(pady=10)
        tk.Button(log_button_frame, text="Edit Selected", command=self.edit_selected_log).pack(side="left", padx=5)
        tk.Button(log_button_frame, text="Delete Selected", command=self.delete_selected_log).pack(side="left", padx=5)
    
    def _on_first_show(self, event=None):
        """Called when dashboard is first shown - ensures proper rendering."""
        # Unbind after first call
        self.unbind("<Map>")
        # Update layout
        self.update_idletasks()
        # Now draw the initial empty chart
        self.update_pie_chart({})

    def refresh_data(self):
        """Fetches and displays the latest user data."""
        if not self.controller.current_user:
            return

        username = self.controller.current_user
        
        # Load data
        user_data = self.controller.data_persistence.load_user_data(username)
        logs = user_data.get('logs', [])
        current_goal, goal_type = self.controller.data_persistence.get_current_goal(username)
        
        # Calculate footprint
        weekly_footprint = self.controller.carbon_calculator.calculate_weekly_total(logs)
        breakdown = self.controller.carbon_calculator.calculate_footprint_by_category(logs)
        
        # Update summary labels
        self.total_footprint_label.config(text=f"Total Footprint (Last 7 Days): {weekly_footprint:.2f} kg CO2e")
        self.goal_label.config(text=f"Weekly Goal: {current_goal:.2f} kg CO2e")
        
        # Update progress bar
        if current_goal > 0:
            progress = min(weekly_footprint / current_goal, 1.0)
            self.progress_label.config(text=f"Progress: {progress*100:.1f}%")
            
            # Force canvas update before drawing
            self.progress_canvas.update_idletasks()
            
            # Draw progress bar
            self.progress_canvas.delete("all")
            canvas_width = self.progress_canvas.winfo_width() if self.progress_canvas.winfo_width() > 1 else 300
            bar_width = int(canvas_width * progress)
            
            if progress < 0.7:
                color = 'green'
            elif progress < 1.0:
                color = 'yellow'
            else:
                color = 'red'
            
            self.progress_canvas.create_rectangle(0, 0, bar_width, 30, fill=color, outline="")
        
        # Update comparison to average
        user_total, system_avg, percentage_diff = self.controller.data_persistence.get_all_weekly_totals_for_comparison(
            username, self.controller.carbon_calculator
        )
        
        if percentage_diff < 0:
            comparison_text = f"System Average: {system_avg:.2f} kg CO2e\nYou are {abs(percentage_diff):.1f}% BELOW average! 🎉"
            comparison_color = "darkgreen"
        elif percentage_diff > 0:
            comparison_text = f"System Average: {system_avg:.2f} kg CO2e\nYou are {percentage_diff:.1f}% above average."
            comparison_color = "darkred"
        else:
            comparison_text = f"System Average: {system_avg:.2f} kg CO2e\nYou are exactly at the average."
            comparison_color = "black"
        
        self.comparison_label.config(text=comparison_text, fg=comparison_color)
        
        # Update contextual tip
        top_category = self.controller.carbon_calculator.get_top_contributing_category(logs)
        tip = get_contextual_tip(top_category)
        self.tip_label.config(text=tip)
        
        # Update activity log
        self.apply_filters()
        
        # Update pie chart - force update of graph_frame first
        self.graph_frame.update_idletasks()
        self.update_pie_chart(breakdown)

    def apply_filters(self):
        """Apply filter and sort to activity log display."""
        if not self.controller.current_user:
            return
        
        logs = self.controller.data_persistence.get_all_activity_logs(self.controller.current_user)
        
        # Apply filter
        filter_category = self.filter_var.get()
        if filter_category != "All":
            logs = [log for log in logs if log.get('category') == filter_category]
        
        # Apply sort
        sort_option = self.sort_var.get()
        if sort_option == "Date (Newest)":
            logs = sorted(logs, key=lambda x: x.get('timestamp', ''), reverse=True)
        elif sort_option == "Date (Oldest)":
            logs = sorted(logs, key=lambda x: x.get('timestamp', ''))
        elif sort_option == "Footprint (High-Low)":
            logs = sorted(logs, key=lambda x: x.get('footprint', 0), reverse=True)
        elif sort_option == "Footprint (Low-High)":
            logs = sorted(logs, key=lambda x: x.get('footprint', 0))
        
        # Update listbox
        self.log_listbox.delete(0, tk.END)
        self.current_displayed_logs = logs  # Store for edit/delete
        
        for i, log in enumerate(logs):
            date_str = log.get('timestamp', 'No Date')[:10]
            activity = log.get('activity', 'N/A')
            footprint = log.get('footprint', 0.0)
            display_text = f"[{i+1}] {date_str} - {activity}: {footprint:.2f} kg CO2e"
            self.log_listbox.insert(tk.END, display_text)

    def update_pie_chart(self, breakdown):
        """Generates and updates the pie chart."""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        labels = [k for k, v in breakdown.items() if v > 0]
        sizes = [v for v in breakdown.values() if v > 0]

        if sizes:
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                               startangle=90, colors=colors)
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_weight('bold')
            ax.axis('equal')
        else:
            ax.text(0.5, 0.5, "No activity logs yet.\nStart logging activities!", 
                   ha='center', va='center', fontsize=11, color='gray')
            ax.axis('off')
        
        # Adjust layout - tighter margins for maximum pie chart size
        self.fig.subplots_adjust(left=0.15, right=0.88, top=0.92, bottom=0.15)
        self.chart.draw()
        
    def edit_selected_log(self):
        """Opens the LogActivityPage to edit the selected log entry."""
        selection = self.log_listbox.curselection()
        if not selection:
            messagebox.showinfo("Edit Log", "Please select an activity log to edit.")
            return

        # Get the log from displayed logs
        displayed_index = selection[0]
        if displayed_index >= len(self.current_displayed_logs):
            return
        
        log_data = self.current_displayed_logs[displayed_index]
        
        # Find the true index in the full log list
        all_logs = self.controller.data_persistence.get_all_activity_logs(self.controller.current_user)
        try:
            true_index = all_logs.index(log_data)
        except ValueError:
            messagebox.showerror("Error", "Could not find log entry.")
            return
        
        # Navigate to edit page
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
            displayed_index = selection[0]
            if displayed_index >= len(self.current_displayed_logs):
                return
            
            log_data = self.current_displayed_logs[displayed_index]
            
            # Find true index
            all_logs = self.controller.data_persistence.get_all_activity_logs(self.controller.current_user)
            try:
                true_index = all_logs.index(log_data)
            except ValueError:
                messagebox.showerror("Error", "Could not find log entry.")
                return
            
            if self.controller.data_persistence.delete_activity_log(self.controller.current_user, true_index):
                messagebox.showinfo("Success", "Activity log deleted.")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to delete activity log.")
    
    def export_data(self):
        """Export activity logs to CSV."""
        if not self.controller.current_user:
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"carbon_tracker_export_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filepath:
            success = self.controller.data_persistence.export_logs_to_csv(
                self.controller.current_user, filepath
            )
            if success:
                messagebox.showinfo("Export Successful", f"Data exported to:\n{filepath}")
            else:
                messagebox.showerror("Export Failed", "Failed to export data.")


# --- Log Activity Page ---

class LogActivityPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padx=20, pady=20)
        self.editing_index = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        tk.Label(self, text="Log Carbon Activity", font=("Arial", 24, "bold")).grid(row=0, column=1, pady=(0, 40))

        # Main Category Dropdown
        tk.Label(self, text="Category:", font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=(10, 0))
        self.category_var = tk.StringVar(self)
        self.category_var.set(list(MAIN_CATEGORIES.keys())[0])
        
        self.category_menu = tk.OptionMenu(self, self.category_var, *MAIN_CATEGORIES.keys(), command=self.update_activity_options)
        self.category_menu.config(font=("Arial", 12), width=30)
        self.category_menu.grid(row=2, column=1, pady=(0, 10), ipady=5, sticky="ew")

        # Specific Activity Dropdown
        tk.Label(self, text="Activity:", font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=(10, 0))
        self.activity_var = tk.StringVar(self)
        
        self.activity_menu = tk.OptionMenu(self, self.activity_var, "")
        self.activity_menu.config(font=("Arial", 12), width=30)
        self.activity_menu.grid(row=4, column=1, pady=(0, 10), ipady=5, sticky="ew")
        
        # Initialize activity options
        self.update_activity_options(self.category_var.get())

        # Value Entry
        tk.Label(self, text="Value (see activity unit):", font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=(10, 0))
        self.value_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.value_entry.grid(row=6, column=1, pady=(0, 10), ipady=5, sticky="ew")

        # Description Entry
        tk.Label(self, text="Description (optional):", font=("Arial", 12)).grid(row=7, column=1, sticky="w", pady=(10, 0))
        self.description_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.description_entry.grid(row=8, column=1, pady=(0, 20), ipady=5, sticky="ew")

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=9, column=1, pady=20)

        self.submit_button = tk.Button(button_frame, text="Submit Log", command=self.handle_submit, width=15, height=2, font=("Arial", 12))
        self.submit_button.pack(side="left", padx=10)

        tk.Button(button_frame, text="Back to Dashboard", command=self.go_back, width=15, height=2, font=("Arial", 12)).pack(side="left", padx=10)
    
    def update_activity_options(self, selected_category):
        """Update the activity dropdown based on selected category."""
        activities = list(MAIN_CATEGORIES[selected_category].keys())
        
        # Clear and rebuild menu
        menu = self.activity_menu["menu"]
        menu.delete(0, "end")
        
        for activity in activities:
            menu.add_command(label=activity, command=lambda value=activity: self.activity_var.set(value))
        
        # Set first activity as default
        if activities:
            self.activity_var.set(activities[0])
        
    def reset_fields(self):
        """Clears fields and resets to default 'add' mode."""
        self.category_var.set(list(MAIN_CATEGORIES.keys())[0])
        self.update_activity_options(self.category_var.get())
        self.value_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.editing_index = None
        self.submit_button.config(text="Submit Log")
        
    def load_for_edit(self, index, log_data):
        """Loads log data into fields for editing."""
        self.editing_index = index
        
        category = log_data.get('category', list(MAIN_CATEGORIES.keys())[0])
        self.category_var.set(category)
        self.update_activity_options(category)
        
        activity = log_data.get('activity', '')
        self.activity_var.set(activity)
        
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, str(log_data.get('value', '')))
        
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, log_data.get('description', ''))
        
        self.submit_button.config(text="Update Log")

    def handle_submit(self):
        """Handles submission (add or update) of the activity log."""
        try:
            value = float(self.value_entry.get())
            if value < 0:
                raise ValueError("Value must be positive")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Value must be a valid positive number.\n{e}")
            return

        category = self.category_var.get()
        activity = self.activity_var.get()
        description = self.description_entry.get()
        
        # Calculate footprint
        footprint = self.controller.carbon_calculator.calculate_footprint(activity, value)
        
        log_data = {
            "category": category,
            "activity": activity,
            "value": value,
            "footprint": footprint,
            "description": description
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
            messagebox.showinfo("Success", f"Activity logged! Footprint: {footprint:.2f} kg CO2e")

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
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        tk.Label(self, text="Set Carbon Reduction Goal", font=("Arial", 24, "bold")).grid(row=0, column=1, pady=(0, 40))

        # Current Goal Display
        self.current_goal_var = tk.StringVar(self)
        tk.Label(self, textvariable=self.current_goal_var, font=("Arial", 14)).grid(row=1, column=1, pady=10)
        
        # Goal Type Selection
        tk.Label(self, text="Goal Type:", font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.goal_type_var = tk.StringVar(value="weekly")
        
        goal_type_frame = tk.Frame(self)
        goal_type_frame.grid(row=3, column=1, pady=(0, 10), sticky="w")
        
        tk.Radiobutton(goal_type_frame, text="Daily", variable=self.goal_type_var, value="daily", font=("Arial", 11)).pack(side="left", padx=10)
        tk.Radiobutton(goal_type_frame, text="Weekly", variable=self.goal_type_var, value="weekly", font=("Arial", 11)).pack(side="left", padx=10)
        
        # Goal Value Entry
        tk.Label(self, text="New Goal (kg CO2e):", font=("Arial", 12)).grid(row=4, column=1, sticky="w", pady=(10, 0))
        self.goal_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.goal_entry.grid(row=5, column=1, pady=(0, 20), ipady=5, sticky="ew")

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=1, pady=20)

        tk.Button(button_frame, text="Set Goal", command=self.handle_set_goal, width=15, height=2, font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back to Dashboard", command=self.go_back, width=15, height=2, font=("Arial", 12)).pack(side="left", padx=10)

    def load_current_goal(self, event=None):
        """Loads and displays the current goal when the page becomes visible."""
        if self.controller.current_user:
            goal_value, goal_type = self.controller.data_persistence.get_current_goal(self.controller.current_user)
            self.current_goal_var.set(f"Current Goal: {goal_value:.2f} kg CO2e ({goal_type})")
            self.goal_type_var.set(goal_type)
            self.goal_entry.delete(0, tk.END)
            self.goal_entry.insert(0, str(goal_value))

    def handle_set_goal(self):
        """Handles the setting of a new carbon goal."""
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

        goal_type = self.goal_type_var.get()
        
        success = self.controller.data_persistence.set_current_goal(user, new_goal, goal_type)
        
        if success:
            messagebox.showinfo("Success", f"{goal_type.capitalize()} goal set to {new_goal:.2f} kg CO2e.")
            self.go_back()
        else:
            messagebox.showerror("Error", "Failed to save new goal.")
            
    def go_back(self):
        """Returns to the dashboard."""
        self.controller.show_frame("DashboardPage")


# --- Timeline Graph Page ---

class TimelineGraphPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="Carbon Footprint Over Time", font=("Arial", 20, "bold")).pack(side="left")
        tk.Button(header_frame, text="← Back to Dashboard", command=lambda: controller.show_frame("DashboardPage")).pack(side="right")
        
        # Date range selector
        control_frame = tk.Frame(self)
        control_frame.pack(fill="x", pady=10)
        
        tk.Label(control_frame, text="Date Range:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.date_range_var = tk.StringVar(value="7")
        date_ranges = [("7 Days", "7"), ("30 Days", "30"), ("90 Days", "90")]
        
        for label, value in date_ranges:
            tk.Radiobutton(control_frame, text=label, variable=self.date_range_var, value=value, 
                          font=("Arial", 11), command=self.refresh_graph).pack(side="left", padx=10)
        
        # Graph frame
        self.graph_frame = tk.Frame(self, bd=2, relief="groove")
        self.graph_frame.pack(fill="both", expand=True, pady=10)
        
        self.fig = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
    
    def refresh_graph(self):
        """Refresh the timeline graph with current data."""
        if not self.controller.current_user:
            return
        
        username = self.controller.current_user
        days = int(self.date_range_var.get())
        
        # Get data
        logs = self.controller.data_persistence.get_all_activity_logs(username)
        daily_data = self.controller.carbon_calculator.calculate_footprint_over_last_n_days(logs, days)
        goal_value, goal_type = self.controller.data_persistence.get_current_goal(username)
        
        # Convert goal to daily if needed
        if goal_type == "weekly":
            daily_goal = goal_value / 7
        else:
            daily_goal = goal_value
        
        # Clear and redraw
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        if daily_data:
            dates = [d['date'] for d in daily_data]
            footprints = [d['footprint'] for d in daily_data]
            
            # Plot footprint line
            ax.plot(dates, footprints, marker='o', linewidth=2, markersize=6, label='Your Footprint', color='steelblue')
            
            # Plot goal line
            ax.axhline(y=daily_goal, color='red', linestyle='--', linewidth=2, label=f'Daily Goal ({daily_goal:.2f} kg)')
            
            # Formatting
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Carbon Footprint (kg CO2e)', fontsize=12)
            ax.set_title(f'Carbon Footprint - Last {days} Days', fontsize=14, fontweight='bold')
            ax.legend(loc='upper left')
            ax.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Highlight days over goal
            for i, fp in enumerate(footprints):
                if fp > daily_goal:
                    ax.plot(dates[i], fp, marker='o', markersize=8, color='red', zorder=5)
        else:
            ax.text(0.5, 0.5, 'No activity data for selected period.', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
        
        self.fig.tight_layout()
        self.canvas.draw()


# --- Main Run Block ---

def run_app():
    """Initializes and runs the application."""
    app = CarbonTrackerApp()
    app.mainloop()

if __name__ == '__main__':
    run_app()