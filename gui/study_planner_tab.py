# TODO: 
#   remove lines 1-9 later
#   ability to add new tasks
#   ability to remove tasks

import sys
from pathlib import Path

# Add project root to sys.path to run this file standalone in VS Code
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.scheduler import (
    SAMPLE_TASKS, 
    DEFAULT_CAPACITY,
    greedy_scheduler, 
    knapsack
)


class StudyPlannerTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        # New Attributes
        self.capacity = tk.StringVar(value=str(DEFAULT_CAPACITY))
        self.tasks = [t.copy() for t in SAMPLE_TASKS]

        self.build_gui()



    def build_gui(self):
        # Title Frame
        title = tk.Label(
            self.frame, text="CSUF Study Planner", font=("Arial", 18, "bold")
        )
        title.pack(pady=10)


        # Text Input Frame
        text_input_frame = tk.Frame(self.frame)
        text_input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            text_input_frame, text="Capacity: "
        ).pack(side="left")

        ttk.Spinbox(
            text_input_frame,
            from_=1, to=24,
            textvariable=self.capacity,
            width=5
        ).pack(side="left")


        # Button Frame
        button_frame = tk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(button_frame, text="Run Greedy", width=15, command=self.run_greedy).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Run Knapsack", width=15, command=self.run_knapsack).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Reset", width=15, command=self.run_reset).grid(row=0, column=2, padx=5)


        # Body Frame
        body_frame = tk.Frame(self.frame)
        body_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #   - Inputs
        input_frame = tk.Frame(body_frame)
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.input_summary_var = tk.StringVar(value=f"Inputs: {len(self.tasks)} tasks")
        tk.Label(input_frame, textvariable=self.input_summary_var,
                font=("Arial", 11, "italic")).pack(pady=2)

        columns = ("name", "start", "end", "duration", "priority")
        self.tree = ttk.Treeview(input_frame, columns=columns, show="headings", height=12)

        self.tree.heading("name", text="Task")
        self.tree.heading("start", text="Start")
        self.tree.heading("end", text="End")
        self.tree.heading("duration", text="Hours")
        self.tree.heading("priority", text="Priority")

        self.tree.column("name", width=200, anchor="w")
        self.tree.column("start", width=60, anchor="center")
        self.tree.column("end", width=60, anchor="center")
        self.tree.column("duration", width=60, anchor="center")
        self.tree.column("priority", width=60, anchor="center")

        self.tree.pack(fill="both", expand=True)


        #   - Outputs
        output_frame = tk.Frame(body_frame)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_summary_var = tk.StringVar(value="Outputs: ")
        tk.Label(output_frame, textvariable=self.output_summary_var,
                font=("Arial", 11, "italic")).pack(pady=2)


        columns = ("name", "start", "end", "duration", "priority")
        self.output_tree = ttk.Treeview(output_frame, columns=columns, show="headings", height=12)

        self.output_tree.heading("name", text="Task")
        self.output_tree.heading("start", text="Start")
        self.output_tree.heading("end", text="End")
        self.output_tree.heading("duration", text="Hours")
        self.output_tree.heading("priority", text="Priority")

        self.output_tree.column("name", width=200, anchor="w")
        self.output_tree.column("start", width=60, anchor="center")
        self.output_tree.column("end", width=60, anchor="center")
        self.output_tree.column("duration", width=60, anchor="center")
        self.output_tree.column("priority", width=60, anchor="center")

        self.output_tree.pack(fill="both", expand=True)

        # Fill Tables
        self.populate_tree()



    # Button press event handlers
    def run_greedy(self):
        self.clear_output()
        total, selected = greedy_scheduler(self.tasks.copy())
        self.output_summary_var.set(f"Greedy: Total priority {total}, {len(selected)} Total tasks scheduled")
        for t in selected:
            self.add_output_row(t)

    def run_knapsack(self):
        self.clear_output()
        try:
            capacity = int(self.capacity.get())
        except ValueError:
            messagebox.showerror("Invalid Capacity", "Please enter a whole number.")
            return
        weights = [t["duration"] for t in self.tasks]
        values  = [t["priority"] for t in self.tasks]
        max_value, items = knapsack(weights, values, capacity)
        self.output_summary_var.set(
            f"Knapsack: Total priority {max_value}, {len(items)} Total tasks scheduled (Capacity {capacity}h)"
        )
        for i in items:
            self.add_output_row(self.tasks[i])

    def run_reset(self):
        self.clear_output()
        self.output_summary_var.set("Run an algorithm to see results.")



    # Helper methods
    def clear_output(self):
        for row in self.output_tree.get_children():
            self.output_tree.delete(row)

    def add_output_row(self, task):
        self.output_tree.insert("", "end", values=(
            task["name"],
            f"{task['start']}:00",
            f"{task['end']}:00",
            task["duration"],
            task["priority"],
    ))

    def populate_tree(self):
        '''Fills table widgets with data'''
        for task in self.tasks:
            self.tree.insert("", "end", values=(
                task["name"],
                f"{task['start']}:00",
                f"{task['end']}:00",
                task['duration'],
                task['priority']
            ))
    
    def refresh_input_tree(self):
        """Update input tree"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.populate_tree()
        self.input_summary_var.set(f"Inputs: {len(self.tasks)} tasks")


        

class TitanCampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TitanCampus Algorithmic Assistant")
        self.root.geometry("950x700")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.create_tabs()

    def create_tabs(self):
        planner_tab = StudyPlannerTab(self.notebook).frame
        self.notebook.add(planner_tab, text="Study Planner")


def main():
    root = tk.Tk()
    app = TitanCampusApp(root)
    root.mainloop()

    return

if __name__ == "__main__":
    main()

