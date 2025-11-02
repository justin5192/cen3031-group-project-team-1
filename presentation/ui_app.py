import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Import necessary core logic components
from data_persistence.data_manager import save_activity_log, load_activity_logs, get_cumulative_footprint
from core_logic.calculator import calculate_footprint
from core_logic.constants import ACTIVITY_CATEGORIES

# --- Helper Functions (Simulating data persistence layer access for GOALS) ---

# SIMULATED: A persistent dictionary to hold the goal for testing PBI 6.1
# In a fully integrated system, this would be part of data_manager/users.json
USER_GOALS = {}

def get_user_goal(username):
    """Retrieves the stored goal for a user (simulated)."""
    return USER_GOALS.get(username, 0.0) # Default to 0.0 if not set

def save_user_goal(username, goal_value):
    """PBI 3.1: Saves goal to user profile (now actually storing it in the global dict)."""
    try:
        goal = float(goal_value)
        USER_GOALS[username] = goal # Store the goal
        return True
    except ValueError:
        return False

# --- Main Application Class ---

class CarbonTrackerApp:
    def __init__(self, master, current_user):
        self.master = master
        master.title(f"CarbonTracker - Logged in as {current_user}")
        self.current_user = current_user
        
        # Check if the goal has been set. If not, start with goal setting.
        if get_user_goal(self.current_user) == 0.0:
            self.show_goal_setting() 
        else:
            self.show_dashboard() 

    def clear_screen(self):
        """Clears all widgets from the current screen."""
        for widget in self.master.winfo_children():
            widget.destroy()

    # --- PBI 3.1 Implementation: Initial Goal Setting ---
    
    def show_goal_setting(self):
        self.clear_screen()
        self.goal_frame = tk.Frame(self.master, padx=10, pady=10)
        self.goal_frame.pack()
        tk.Label(self.goal_frame, text="Set Your Initial Reduction Goal", font=('Arial', 14, 'bold')).pack(pady=10)
        tk.Label(self.goal_frame, text="What is your target weekly CO2e reduction (in kg)?").pack(pady=5)
        self.goal_entry = tk.Entry(self.goal_frame, width=30)
        self.goal_entry.pack(pady=5)
        tk.Label(self.goal_frame, text="(Default period: Weekly)").pack()
        tk.Button(self.goal_frame, text="Set Goal and Continue", command=self.handle_set_goal).pack(pady=20)

    def handle_set_goal(self):
        goal_value = self.goal_entry.get()
        if not goal_value:
            messagebox.showerror("Input Error", "Please enter a numerical reduction goal.")
            return
        if save_user_goal(self.current_user, goal_value):
            messagebox.showinfo("Success", f"Your goal of {goal_value} kg CO2e/week has been set!")
            self.show_dashboard() # Navigate to Dashboard after setting the goal
        else:
            messagebox.showerror("Input Error", "The goal must be a valid number.")

    # --- PBI 4.2 Implementation: Activity Logging Form (Now accessible via Dashboard) ---
    def show_activity_logging_form(self):
        self.clear_screen()
        self.log_frame = tk.Frame(self.master, padx=20, pady=20)
        self.log_frame.pack()

        tk.Label(self.log_frame, text="Log a New Activity", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Activity Type Selection
        tk.Label(self.log_frame, text="1. Activity Type:").grid(row=1, column=0, sticky='w', pady=5)
        self.activity_types = list(ACTIVITY_CATEGORIES.keys())
        self.selected_activity = tk.StringVar(self.log_frame)
        self.selected_activity.set(self.activity_types[0])
        self.activity_menu = tk.OptionMenu(self.log_frame, self.selected_activity, *self.activity_types, command=self._update_subcategory_menu)
        self.activity_menu.config(width=20)
        self.activity_menu.grid(row=1, column=1, sticky='ew', padx=10)

        # Sub-Category/Detail Selection
        tk.Label(self.log_frame, text="2. Detail/Sub-Category:").grid(row=2, column=0, sticky='w', pady=5)
        self.sub_categories = ACTIVITY_CATEGORIES[self.selected_activity.get()]
        self.selected_sub_category = tk.StringVar(self.log_frame)
        self.selected_sub_category.set(self.sub_categories[0])
        self.subcategory_menu = tk.OptionMenu(self.log_frame, self.selected_sub_category, *self.sub_categories)
        self.subcategory_menu.config(width=20)
        self.subcategory_menu.grid(row=2, column=1, sticky='ew', padx=10)
        
        # Value Input
        tk.Label(self.log_frame, text="3. Value (Miles/Servings/kWh):").grid(row=3, column=0, sticky='w', pady=5)
        self.value_entry = tk.Entry(self.log_frame, width=23)
        self.value_entry.grid(row=3, column=1, sticky='ew', padx=10)

        # Log Button
        tk.Button(self.log_frame, text="Calculate & Log Activity", command=self.handle_log_activity, bg='green', fg='white').grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Back to Dashboard
        tk.Button(self.master, text="<< Back to Dashboard", command=self.show_dashboard).pack(pady=10)


    def _update_subcategory_menu(self, *args):
        """Updates the Sub-Category dropdown options when the main Activity Type changes."""
        activity_type = self.selected_activity.get()
        menu = self.subcategory_menu["menu"]
        menu.delete(0, "end")
        
        self.sub_categories = ACTIVITY_CATEGORIES.get(activity_type, [])
        if self.sub_categories:
            self.selected_sub_category.set(self.sub_categories[0])
            for sub_cat in self.sub_categories:
                menu.add_command(label=sub_cat, command=tk._setit(self.selected_sub_category, sub_cat))
        else:
            self.selected_sub_category.set("N/A")

    def handle_log_activity(self):
        activity_type = self.selected_activity.get()
        sub_category = self.selected_sub_category.get()
        value_str = self.value_entry.get()

        try:
            value = float(value_str)
            if value <= 0:
                 messagebox.showerror("Input Error", "Value must be greater than zero.")
                 return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the value.")
            return

        footprint_kgCO2e = calculate_footprint(activity_type, sub_category, value)

        new_log_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activity_type": activity_type,
            "sub_category": sub_category,
            "value": value,
            "footprint": footprint_kgCO2e
        }

        save_activity_log(self.current_user, new_log_entry)

        messagebox.showinfo(
            "Log Success",
            f"Logged {value} of {sub_category}.\nFootprint: {footprint_kgCO2e} kg CO2e"
        )
        self.value_entry.delete(0, tk.END)
        self.show_dashboard() # Show the dashboard now to reflect the updated total

    # --- PBI 6.1 & PBI 9.1 Combined Dashboard ---

    def show_dashboard(self):
        self.clear_screen()
        
        # --- TOP SECTION: GOAL PROGRESS (PBI 6.1) ---
        dashboard_frame = tk.Frame(self.master, padx=20, pady=10)
        dashboard_frame.pack(pady=10)
        
        # Use the data_manager function now that it's implemented there
        current_footprint = get_cumulative_footprint(self.current_user) 
        target_goal = get_user_goal(self.current_user)
        
        tk.Label(dashboard_frame, text="Carbon Tracker Dashboard", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # 1. Display Current Footprint
        tk.Label(dashboard_frame, text="Current Cumulative Footprint:", font=('Arial', 12)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        tk.Label(dashboard_frame, text=f"{current_footprint:.2f} kg CO2e", font=('Arial', 12, 'bold'), fg='blue').grid(row=1, column=1, sticky='e', padx=5, pady=5)

        # 2. Display Goal
        tk.Label(dashboard_frame, text="Weekly Reduction Goal:", font=('Arial', 12)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        tk.Label(dashboard_frame, text=f"{target_goal:.2f} kg CO2e", font=('Arial', 12, 'bold'), fg='green').grid(row=2, column=1, sticky='e', padx=5, pady=5)

        # 3. Status/Delta Display
        delta = target_goal - current_footprint
        
        if delta > 0:
            status_text = f"You are {delta:.2f} kg CO2e BELOW your reduction goal!"
            status_color = 'green'
        elif delta < 0:
            status_text = f"You are {-delta:.2f} kg CO2e ABOVE your reduction goal!"
            status_color = 'red'
        else:
            status_text = "You have exactly met your reduction goal!"
            status_color = 'orange'
            
        tk.Label(dashboard_frame, text=status_text, font=('Arial', 12, 'italic'), fg=status_color).grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Frame(self.master, height=2, bd=1, relief='sunken').pack(fill='x', padx=10, pady=5) # Separator

        # --- BOTTOM SECTION: ACTIVITY LOG (PBI 9.1) ---
        tk.Label(self.master, text="Recent Activity Log (PBI 9.1)", font=('Arial', 14, 'bold')).pack(pady=5)
        
        log_key = f"{self.current_user}_logs"
        all_logs = load_activity_logs()
        user_logs = all_logs.get(log_key, [])

        if not user_logs:
            tk.Label(self.master, text="No activities logged yet. Log one now!").pack(pady=5)
        else:
            log_container = tk.Frame(self.master)
            log_container.pack(fill='both', expand=True, padx=10, pady=5)
            log_text = tk.Text(log_container, wrap='word', height=10, width=60)
            scrollbar = tk.Scrollbar(log_container, command=log_text.yview)
            log_text.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            log_text.pack(side='left', fill='both', expand=True)

            display_text = "Date/Time | Type | Detail | Value | Footprint (kg CO2e)\n"
            display_text += "=" * 70 + "\n"
            
            # Display only the last 5 logs for a concise dashboard
            for entry in reversed(user_logs[-5:]): 
                date = entry.get('date', 'N/A').split(' ')[0]
                activity_type = entry.get('activity_type', 'N/A')
                sub_category = entry.get('sub_category', 'N/A')
                value = entry.get('value', 0)
                footprint = entry.get('footprint', 0.0)

                line = f"{date} | {activity_type.ljust(12)} | {sub_category.ljust(10)} | {str(value).ljust(5)} | {footprint:.2f}\n"
                display_text += line
            
            log_text.insert(tk.END, display_text)
            log_text.config(state='disabled')

        # --- BOTTOM ACTION BUTTONS ---
        action_frame = tk.Frame(self.master)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text="Log New Activity (PBI 4.2)", command=self.show_activity_logging_form).pack(side='left', padx=10)
        # Placeholder for the next major PBI
        tk.Button(action_frame, text="Edit/Delete Logs (PBI 5.1 - Next)", state='disabled').pack(side='left', padx=10)


# --- Main Application Execution (For testing purposes) ---
if __name__ == "__main__":
    # Simulate a successful login/registration for a user
    mock_user = "Donald"
    root = tk.Tk()
    app = CarbonTrackerApp(root, mock_user)
    root.mainloop()
