# CarbonTracker Project Handoff: Sprint 2 Feature Complete

# 

# This README documents the core functionality completed up through the final feature of Sprint 2 (PBI 5.2) and outlines the prioritized tasks for the start of Sprint 3.

# 

# 🚀 How to Run the Program

# 

# The application is built using Python with the Tkinter library for the graphical user interface.

# 

# Dependencies: Ensure you have Python 3.10+ installed. The project relies only on standard Python libraries (os, json, hashlib, tkinter).

# 

# Environment: Navigate to the root directory of the project in your terminal.

# 

# Execution: Run the main UI application file:

# 

# python presentation/ui\_app.py

# 

# 

# ✅ New Features Added (PBI 5.1 / 5.2 Completion)

# 

# The primary focus of this update was implementing full Edit and Delete functionality for activity logs, moving the project beyond read-only functionality.

# 

# Feature

# 

# Component Updated

# 

# Description

# 

# Selectable Activity Log

# 

# presentation/ui\_app.py

# 

# The dashboard log display (PBI 9.1) has been refactored from a read-only tk.Text widget to a tk.Listbox, allowing users to click and select a specific activity entry.

# 

# Edit/Delete UI \& Handlers

# 

# presentation/ui\_app.py

# 

# A dedicated form appears upon selecting an activity, allowing users to view, modify, or delete the selected log entry.

# 

# Data Persistence Logic

# 

# data\_persistence/data\_manager.py

# 

# Implemented update\_activity\_log(username, index, new\_log\_data) and delete\_activity\_log(username, index) to correctly modify the underlying JSON log files.

# 

# 🛠️ Next Steps: Sprint 3 Priority Tasks

# 

# The project is now fully focused on Priority 2 (High Value/Core Visuals) features. We are currently targeting the Core Visualization \& Aggregation PBIs.

# 

# Focus: Core Logic and Data Aggregation

# 

# PBI ID

# 

# Description

# 

# Est. Points

# 

# Required File Update

# 

# 8.1

# 

# Implement aggregation logic to summarize total footprint by category (e.g., Transportation: 50 kgCO2).

# 

# 2

# 

# core\_logic/calculator.py

# 

# 7.1

# 

# Implement the core logic/data preparation for a plot showing total footprint over the last 7 days.

# 

# 3

# 

# core\_logic/calculator.py

# 

# 13.1

# 

# Implement function to dump all current log data to a basic export file (CSV or JSON export).

# 

# 2

# 

# data\_persistence/data\_manager.py

# 

# The best place to start is PBI 8.1 by adding the category aggregation method to core\_logic/calculator.py.

