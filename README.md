CARBONTRACKER - INDIVIDUAL CARBON FOOTPRINT TRACKING

Project Goal: To create a basic tool to track, reduce, and visualize an individual's carbon footprint for academic evaluation.

TEAM ROLES AND OWNERSHIP

| Project Role | Team Member(s) | Primary Responsibility Layer |
| Science Lead | Lance Daley | Scientific Data and Conversion Factors (Core Logic) |
| Front-End | Donald Lynch | User Interface (UI) / Presentation Layer |
| Dev Team | Justin Williamson, Blake McGahee | Core Logic and Data Persistence Layer |

TECHNOLOGY AND ARCHITECTURE

The project implements a Layered Architecture (Presentation, Core Logic, Data Persistence) to ensure clear separation of concerns.

Component: Language | Technology: Python 3.10+ | Layer: Core development platform.

Component: UI Framework | Technology: Tkinter | Layer: Presentation Layer

Component: Data Storage | Technology: Local JSON Files | Layer: Data Persistence Layer

Component: Security | Technology: hashlib (PBKDF2) | Layer: Core Logic Layer (Authentication)

PROJECT STRUCTURE

The code is organized into three distinct layers:

CarbonTracker/
├── .venv/                         # Isolated Python Virtual Environment
├── core_logic/                    # Application/Business Logic Layer
│   ├── auth.py                    # User Auth/Security (PBI 1.2, 2.1)
│   ├── calculator.py              # Footprint Calculation (PBI 4.3)
│   └── constants.py               # Scientific Conversion Factors (PBI 4.1)
├── data_persistence/              # Data Persistence Layer
│   └── data_manager.py            # JSON Read/Write Operations (PBI 1.1, 4.4)
├── data_storage/                  # External File System (Data Storage Location)
│   ├── activity_logs.json         # Logged activity data
│   └── users.json                 # User profiles and hashed credentials
├── presentation/                  # Presentation Layer (UI)
│   └── ui_app.py                  # Tkinter application and UI flow (PBI 3.1, 4.2, 9.1)
└── main.py                        # Application Entry Point

SPRINT 1 STATUS: CORE FOUNDATION COMPLETE

The Dev and Science Lead teams have completed all Priority 1 backend PBIs. Focus is now on UI integration.

| PBI | Product Backlog Item | Status | Owner |
| 1.1 | Design file storage structure. | COMPLETE | Dev |
| 1.2 | Implement user registration (hashing/salting). | COMPLETE | Dev |
| 2.1 | Implement basic authentication check. | COMPLETE | Dev |
| 4.1 | Define footprint conversion factors. | COMPLETE | Science Lead |
| 4.3 | Implement footprint calculation logic. | COMPLETE | Dev / Science Lead |
| 4.4 | Implement function to save activity log. | COMPLETE | Dev |
| 3.1 | Implement goal setting input field. | IN PROGRESS | Front-End |
| 4.2 | Implement activity logging form (UI). | IN PROGRESS | Front-End |
| 9.1 | Implement simple activity log display (UI). | IN PROGRESS | Front-End |

SETUP AND RUNNING THE PROJECT

Clone the Repository

git clone https://github.com/justin5192/cen3031-group-project-team-1.git
cd cen3031-group-project-team-1

Activate Virtual Environment

source .venv/Scripts/activate

Run the UI Application

python presentation/ui_app.py

CONTRIBUTION AND GIT WORKFLOW

The master branch is PROTECTED and requires Pull Requests (PRs) for all updates.

Pull: Start every session by synchronizing with the latest remote changes:

git pull origin master

Code: Create a new feature branch for your task (e.g., git checkout -b feature/pbi-42-logging-form).

Push: Push your local commits to your new branch (git push -u origin feature/branch-name).

Pull Request: Create a PR on GitHub from your feature branch into master for review and merging.
