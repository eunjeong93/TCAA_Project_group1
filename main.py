
import tkinter as tk
from tkinter import ttk

from gui.campus_navigator_tab import CampusNavigatorTab
from gui.study_planner_tab import StudyPlannerTab
from gui.note_search_tab import NoteSearchTab

class TitanCampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TitanCampus Algorithmic Assistant")
        self.root.geometry("950x700")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.create_tabs()

    def create_tabs(self):
        campus_tab = CampusNavigatorTab(self.notebook)
        planner_tab = StudyPlannerTab(self.notebook).frame
        self.notebook.add(campus_tab.frame, text="Campus Navigator")
        self.notebook.add(planner_tab, text="Study Planner")
        self.notebook.add(NoteSearchTab(self.notebook), text="Notes Search")


if __name__ == "__main__":
    root = tk.Tk()
    app = TitanCampusApp(root)
    root.mainloop()