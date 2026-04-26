# TitanCampus Algorithmic Assistant (TCAA)

## Project Overview

TitanCampus Algorithmic Assistant (TCAA) is a Python GUI application built for CPSC 335 Algorithm Engineering.  
This project demonstrates several major algorithmic concepts through an interactive desktop application.

The application currently includes:

1. Campus Navigator
2. Study Planner
3. Notes Search Engine

Each module focuses on a different algorithmic topic, including graph algorithms, greedy algorithms, dynamic programming, and string pattern matching.

---

## Technologies Used

- Python 3.x
- Tkinter
- heapq
- collections
- time
- PyPDF2
- python-docx

---

## Project Structure

```text
TCAA_Project_group1/
│
├── main.py
├── README.md
├── requirements.txt
│
├── algorithms/
│   ├── __init__.py
│   ├── graph_algorithms.py
│   ├── scheduler.py
│   └── string_search.py
│
├── gui/
│   ├── __init__.py
│   ├── campus_navigator_tab.py
│   ├── study_planner_tab.py
│   └── note_search_tab.py
│
└── utils/
    ├── __init__.py
    └── file_loader.py
```

---

## How to Run the Project

### 1. Open the project folder

```bash
cd /TCAA_Project_group1
```

### 2. Install required dependencies

```bash
python -m pip install -r requirements.txt
```

If needed, install the packages directly:

```bash
python -m pip install PyPDF2 python-docx
```

### 3. Run the application

```bash
python main.py
```

The application should open as a Tkinter GUI with multiple tabs.

---