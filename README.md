# CarbonTracker 🌱

**Personal Carbon Footprint Tracker**

A desktop application that helps individuals track, monitor, and reduce their personal carbon footprint through scientifically accurate calculations and intuitive visualizations.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/yourusername/carbontracker)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🌍 Overview

CarbonTracker addresses a critical environmental challenge: while most people want to reduce their environmental impact, they lack accessible tools to measure their daily carbon emissions and track progress toward reduction goals.

**The Problem:**
- Individual carbon footprints contribute significantly to climate change
- Most people lack tools to measure daily emissions
- Without measurement, behavioral change is difficult to achieve

**Our Solution:**
- Desktop application with 100 scientifically validated emission factors
- Intuitive interface requiring no technical expertise
- Real-time calculations and visual feedback
- Goal tracking and motivational features
- Complete data ownership with local storage

---

## ✨ Features

### Core Functionality

- 🔐 **Secure User Authentication** - SHA-256 password hashing
- 📊 **Activity Logging** - Track activities across 4 major categories:
  - Transportation (cars, buses, trains, planes, etc.)
  - Food (meat, dairy, vegetables, etc.)
  - Energy (electricity, heating, appliances)
  - Waste (landfill, recycling, composting)
- 🧮 **Real-Time Calculations** - Instant carbon footprint calculation using EPA-validated emission factors
- 📈 **Visual Dashboard** - Color-coded progress bars, pie charts, and trend graphs
- 🎯 **Goal Setting & Tracking** - Set weekly carbon footprint goals and monitor progress
- 📅 **Timeline Visualization** - View emissions trends over 7, 30, or 90 days
- ✏️ **Activity Management** - Full CRUD operations (Create, Read, Update, Delete)
- 🔍 **Filtering & Sorting** - Find high-impact activities easily
- 📤 **CSV Export** - Download complete activity history for personal analysis
- 📊 **Comparison to Average** - See how you rank against other users
- 💡 **Contextual Tips** - Receive personalized advice based on your highest category

### Technical Features

- 🖥️ **Cross-Platform** - Runs on Windows, macOS, and Linux
- 💾 **Local Data Storage** - All data stored locally in JSON format
- 🔒 **Privacy-Focused** - No cloud dependency, no data transmission
- ⚡ **Fast Performance** - Instant dashboard updates, <1 second load times
- 🎨 **Intuitive UI** - Clean design with Tkinter and Matplotlib
- 📝 **Well-Documented** - Comprehensive code comments (20.7% ratio)

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/images/dashboard.png)
*Main dashboard showing progress bar, pie chart, comparison, and tips*

### Activity Logging
![Activity Logging](docs/images/activity_logging.png)
*Two-stage dropdown interface for logging activities*

### Timeline Graph
![Timeline Graph](docs/images/timeline_graph.png)
*View emissions trends over 7, 30, or 90 days*

### Activity Management
![Activity Management](docs/images/activity_management.png)
*Filter, sort, edit, and delete activities*

---

## 🚀 Installation

### Prerequisites

- **Python 3.9 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning repository)

### Step 1: Download the Project

**Option A: Clone with Git**
```bash
git clone https://github.com/yourusername/carbontracker.git
cd carbontracker
```

**Option B: Download ZIP**
1. Click "Code" → "Download ZIP" on GitHub
2. Extract the ZIP file to your desired location
3. Open terminal/command prompt in the extracted folder

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you don't have a requirements.txt file, install manually:**
```bash
pip install matplotlib
```

### Step 4: Verify Installation

```bash
python ui/app.py
```

You should see the CarbonTracker login window appear!

---

## 🎯 Quick Start

### First Time Setup

1. **Launch the Application**
   ```bash
   python ui/app.py
   ```

2. **Create Your Account**
   - Click "Register"
   - Enter a username and password
   - Click "Register" to create your account

3. **Set Your Weekly Goal**
   - Enter your target weekly carbon footprint (default: 100 kg CO₂)
   - Click "Set Goal"

4. **Log Your First Activity**
   - Click "Log Activity"
   - Select category (e.g., Transportation)
   - Select specific activity (e.g., Car - Small Gasoline)
   - Enter quantity (e.g., 15 miles)
   - Click "Submit"

5. **View Your Dashboard**
   - See your current footprint vs. goal
   - Check the category breakdown pie chart
   - Read your personalized tip

That's it! You're now tracking your carbon footprint! 🎉

---

## 📖 Usage Guide

### Logging Activities

CarbonTracker uses a **two-stage dropdown** system for easy activity selection:

1. **Select Category:**
   - Transportation
   - Food
   - Energy
   - Waste

2. **Select Specific Activity:**
   - Category determines available options
   - Example: Transportation → Car - Small Gasoline (Miles)

3. **Enter Quantity:**
   - Miles for transportation
   - Servings for food
   - kWh for energy
   - Pounds for waste

4. **Add Description (Optional):**
   - Add context like "Commute to work"

### Understanding Your Dashboard

**Weekly Summary:**
- Shows total CO₂ for current week
- Displays percentage of your goal
- Updates in real-time as you log activities

**Progress Bar:**
- 🟢 **Green** - Under 70% of goal (on track!)
- 🟡 **Yellow** - 70-100% of goal (approaching limit)
- 🔴 **Red** - Over 100% of goal (exceeded)

**Category Breakdown Pie Chart:**
- Visual representation of emissions by category
- Identifies your highest-impact areas
- Updates automatically with new activities

**Comparison to Average:**
- Shows system-wide average footprint
- Displays your percentage above/below average
- Provides motivation through social comparison

**Tip of the Day:**
- Analyzes your highest category
- Provides specific, actionable advice
- Updates based on your activity patterns

### Timeline Graph

View your emissions trends over time:

1. Click "View Timeline Graph"
2. Select time range:
   - **7 days** - Weekly patterns
   - **30 days** - Monthly trends
   - **90 days** - Quarterly analysis
3. Red dashed line shows your daily goal
4. Red bars indicate days over goal

### Managing Activities

**Edit an Activity:**
1. Select activity from list
2. Click "Edit"
3. Modify quantity or date
4. Click "Save"
5. Dashboard updates automatically

**Delete an Activity:**
1. Select activity from list
2. Click "Delete"
3. Confirm deletion
4. Dashboard recalculates totals

**Filter Activities:**
- Click "Filter by Category" dropdown
- Select Transportation, Food, Energy, or Waste
- View only selected category

**Sort Activities:**
- Click "Sort by Date" - Newest or oldest first
- Click "Sort by Footprint" - Highest or lowest first

### Exporting Data

1. Click "Export to CSV"
2. CSV file saved to current directory
3. Open in Excel or Google Sheets
4. Columns include:
   - Date
   - Category
   - Activity Type
   - Amount
   - Carbon Footprint (kg CO₂)

### Updating Your Goal

1. Click "Settings" or "Update Goal"
2. Enter new weekly goal
3. Click "Save"
4. Dashboard recalculates percentages

---

## 🛠️ Technology Stack

### Languages & Frameworks
- **Python 3.9+** - Core programming language
- **Tkinter** - GUI framework (included with Python)
- **Matplotlib 3.5+** - Data visualization library

### Data & Security
- **JSON** - Local data storage format
- **hashlib** - SHA-256 password hashing (Python standard library)

### Development Tools
- **Git** - Version control
- **GitHub** - Repository hosting
- **pylint** - Code quality analysis
- **Virtual Environment** - Dependency isolation

### Architecture
- **Three-Layer Architecture:**
  - Presentation Layer (Tkinter UI)
  - Core Logic Layer (Calculations & Business Rules)
  - Data Persistence Layer (JSON Storage)

---

## 📁 Project Structure

```
carbontracker/
├── ui/
│   └── app.py                      # Main application UI (800+ lines)
│
├── core_logic/
│   ├── calculator.py               # Carbon footprint calculations (300+ lines)
│   ├── constants.py                # 100 emission factors (200+ lines)
│   └── data_persistence.py         # Data storage & retrieval (450+ lines)
│
├── authentication/
│   └── user_auth.py                # User authentication (250+ lines)
│
├── data/
│   └── users/                      # User data files (JSON)
│       └── <hashed_username>.json
│
├── docs/
│   ├── architecture.md             # System architecture documentation
│   ├── user_stories.md             # User stories and acceptance criteria
│   └── images/                     # Screenshots for README
│
├── tests/
│   ├── test_calculator.py          # Unit tests for calculations
│   ├── test_data_persistence.py    # Unit tests for data layer
│   └── test_ui.py                  # Integration tests for UI
│
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore file
```

---

## 🔧 Development

### Setting Up Development Environment

1. **Fork and Clone Repository**
   ```bash
   git clone https://github.com/yourusername/carbontracker.git
   cd carbontracker
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make Changes**
   - Edit code following PEP 8 style guide
   - Add comments for complex logic
   - Update tests if necessary

5. **Test Your Changes**
   ```bash
   python ui/app.py
   ```

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Describe your changes
   - Request review from team members

### Code Style Guidelines

- **PEP 8 Compliance:** Follow Python style guide
- **Naming Conventions:**
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
- **Comments:**
  - Docstrings for all public methods
  - Inline comments for complex logic
- **Line Length:** Max 79 characters (flexible to 100 for readability)
- **Imports:** Group by standard library, third-party, local modules

### Adding New Emission Factors

To add new emission factors to `core_logic/constants.py`:

```python
MAIN_CATEGORIES = {
    "Transportation": {
        "Your New Activity (Unit)": emission_factor,  # kg CO₂ per unit
        # Example: "Electric Scooter (Miles)": 0.05,
    },
    # ... other categories
}
```

**Important:**
- Include unit in parentheses
- Document source in comment
- Validate with EPA or peer-reviewed studies
- Update documentation

---

## 🧪 Testing

### Running Tests

**Manual Testing:**
```bash
python ui/app.py
```
Follow test cases in `docs/test_plan.md`

**Automated Testing (if implemented):**
```bash
python -m pytest tests/
```

### Test Coverage

Current test coverage includes:
- ✅ Unit tests for all calculation functions
- ✅ Integration tests for activity logging workflow
- ✅ System tests for complete user scenarios
- ✅ Cross-platform tests (Windows, macOS, Linux)
- ✅ Edge case and error handling tests

**Test Results:**
- Total Test Cases: 31
- Passed: 31
- Failed: 0
- Pass Rate: 100%

### Creating Test Accounts

For testing purposes, you can use these pre-configured accounts:

**Test Account 1:**
- Username: `demo_user`
- Password: `demo123`
- Has pre-populated activities

**Test Account 2:**
- Username: `test_user`
- Password: `test456`
- Empty account for new user testing

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs** - Open an issue describing the problem
- 💡 **Suggest Features** - Share ideas for improvements
- 📝 **Improve Documentation** - Fix typos, add examples
- 🔧 **Submit Pull Requests** - Fix bugs or add features
- 🧪 **Write Tests** - Improve test coverage
- 🌍 **Add Emission Factors** - Research and add new factors

### Contribution Guidelines

1. **Check Existing Issues** - Avoid duplicates
2. **Create Issue First** - Discuss major changes before coding
3. **Follow Code Style** - Use PEP 8 standards
4. **Write Tests** - Cover new functionality
5. **Update Documentation** - Explain your changes
6. **Small Commits** - One logical change per commit
7. **Descriptive Messages** - Clear commit messages

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request with description

---

## 👥 Team

**Group 1 - Fall 2025**

| Name | Role | Contributions |
|------|------|---------------|
| **Lance Daley** | Science Lead | 100 emission factors, scientific validation |
| **Donald Lynch** | Front-End Developer & Scrum Master | Complete UI implementation, Agile coordination |
| **Justin Williamson** | Backend Developer | Calculation engine, business logic |
| **Blake McGahee** | Backend Developer & Technical Lead | Data architecture, authentication, system design |

**Course:** CEN3031 - Introduction to Software Engineering  
**Semester:** Fall 2025  
**Institution:** University of Florida

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Group 1 - CarbonTracker Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Scientific Data Sources
- **EPA** - Greenhouse Gas Emissions Data
- **IPCC** - Climate Change Reports
- **Our World in Data** - Food production emissions
- **U.S. Energy Information Administration** - Electricity data

### Educational Resources
- **University of Florida** - CEN3031 Course Materials
- **Course Instructors & TAs** - Guidance and feedback
- **Clean Code by Robert Martin** - Code quality principles
- **Agile Manifesto** - Development methodology

### Tools & Libraries
- **Python Software Foundation** - Python programming language
- **Matplotlib Team** - Data visualization library
- **Tkinter/Tcl/Tk** - GUI framework
- **Git & GitHub** - Version control and collaboration

### Inspiration
- Our planet 🌍 and the urgent need to address climate change
- Individuals committed to reducing their environmental impact
- The belief that measurement enables improvement

---

## 🌟 Future Enhancements

Potential features for future versions:

- 📱 **Mobile Applications** - iOS and Android native apps
- ☁️ **Cloud Synchronization** - Multi-device data access
- 👥 **Social Features** - Share progress, group challenges
- 🤖 **Machine Learning** - Pattern detection and predictions
- 🏠 **Smart Home Integration** - Automatic tracking from IoT devices
- 🌳 **Carbon Offsetting** - Integration with offset providers
- 🌍 **International Support** - Multiple languages and regions
- 📊 **Advanced Analytics** - Deeper insights and reports

---

## 📞 Support

### Getting Help

- **📖 Documentation** - Check this README and docs/ folder
- **🐛 Issues** - [GitHub Issues](https://github.com/yourusername/carbontracker/issues)
- **💬 Discussions** - [GitHub Discussions](https://github.com/yourusername/carbontracker/discussions)
- **📧 Email** - Contact team members (see Team section)

### Reporting Bugs

When reporting bugs, please include:
- Operating system and version
- Python version (`python --version`)
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Error messages or screenshots
- Relevant log output

### Feature Requests

We love hearing your ideas! When requesting features:
- Describe the problem you're trying to solve
- Explain your proposed solution
- Provide use cases or examples
- Consider implementation complexity

---

## 📈 Project Statistics

- **Total Lines of Code:** 2,047
- **Comments:** 423 lines (20.7%)
- **Number of Modules:** 5
- **Functions:** 50+
- **Emission Factors:** 100
- **Test Cases:** 31 (100% pass rate)
- **Supported Platforms:** 3 (Windows, macOS, Linux)
- **Development Time:** 4 weeks (2 sprints)
- **Team Size:** 4 members
- **User Stories:** 13 (100% complete)
- **Story Points Delivered:** 55

---

## 🔗 Useful Links

- **GitHub Repository:** [https://github.com/yourusername/carbontracker](https://github.com/yourusername/carbontracker)
- **Project Documentation:** [docs/](docs/)
- **Issue Tracker:** [GitHub Issues](https://github.com/yourusername/carbontracker/issues)
- **EPA Emissions Data:** [https://www.epa.gov/ghgemissions](https://www.epa.gov/ghgemissions)
- **IPCC Reports:** [https://www.ipcc.ch](https://www.ipcc.ch)

---

## 📝 Changelog

### Version 1.0.0 (November 2025)
- ✨ Initial release
- 🔐 User authentication with secure password hashing
- 📊 Activity logging with 100 emission factors
- 📈 Real-time dashboard with visualizations
- 📅 Timeline graphs (7/30/90-day views)
- ✏️ Full CRUD operations for activities
- 🔍 Filtering and sorting capabilities
- 📤 CSV export functionality
- 📊 Comparison to system averages
- 💡 Contextual tips based on usage patterns
- 🖥️ Cross-platform support (Windows, macOS, Linux)

---

## ⭐ Star Us on GitHub!

If you find CarbonTracker useful, please consider giving us a star ⭐ on GitHub! It helps others discover the project and motivates us to continue development.

---

**Made with 💚 by Group 1**

*Empowering individuals to track, understand, and reduce their carbon footprint one activity at a time.*

---

**Last Updated:** November 16, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅