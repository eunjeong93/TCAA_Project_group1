import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.graph_algorithms import (
    CAMPUS_GRAPH,
    bfs_path,
    is_connected_to,
    dijkstra_shortest_path,
    prim_mst
)

BUILDING_LAYOUT = {
    # West / Left side
    "ASC":  (10, 360, 60, 410),
    "TH":   (20, 420, 80, 480),
    "TSU":  (80, 330, 160, 400),
    "VA":   (95, 420, 170, 480),
    "NPS":  (95, 520, 190, 590),
    "E3":   (95, 595, 160, 640),
    "UP":   (85, 250, 140, 300),
    "SCPS": (145, 250, 220, 305),
    "SRC":  (225, 250, 305, 305),

    # North / Sports area
    "TSC":  (330, 70, 390, 120),
    "TS":   (250, 75, 320, 140),
    "AF":   (430, 80, 500, 145),
    "GF":   (405, 20, 480, 70),
    "IF":   (330, 155, 400, 225),
    "EP":   (425, 155, 495, 225),
    "TTC":  (255, 165, 320, 230),
    "TTF":  (255, 115, 330, 165),   # optional if used later
    "TSF":  (505, 145, 575, 210),

    # Upper center
    "TG":   (330, 245, 425, 305),
    "KHS":  (260, 275, 350, 335),
    "SHCC": (505, 270, 575, 320),
    "RG":   (590, 250, 635, 300),

    # Center campus
    "B":    (230, 345, 300, 405),
    "PL":   (360, 365, 430, 435),
    "ECS Lawn": (455, 330, 545, 405),
    "EC":   (445, 430, 515, 490),
    "CPAC": (185, 455, 310, 535),
    "GC":   (300, 535, 360, 585),
    "MH":   (370, 520, 470, 590),
    "DBH":  (300, 590, 420, 640),
    "MC":   (430, 610, 500, 645),

    # East center / academic buildings
    "E":    (575, 345, 635, 405),
    "CS":   (640, 345, 700, 405),
    "E1":   (590, 455, 675, 535),
    "H":    (510, 510, 585, 570),
    "GH":   (585, 565, 655, 625),
    "LH":   (500, 610, 565, 650),
    "SGMH": (650, 610, 735, 650),

    # East / housing and parking
    "RH":   (685, 170, 770, 250),
    "TDH":  (700, 270, 785, 330),
    "ENPS": (715, 390, 810, 460),
    "ESPS": (715, 480, 810, 550),

    # South / lower campus
    "E2":   (215, 600, 285, 645),
}
class CampusNavigatorTab:
    def __init__(self, parent):
        self.map_y_offset = 45
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.building_items = {}
        self.path_items = []
        self.build_gui()

    def build_gui(self):
        title = tk.Label(
            self.frame,
            text="Campus Navigator - CSUF Block Map",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        top_frame = tk.Frame(self.frame)
        top_frame.pack(fill="x", padx=10, pady=5)

        buildings = sorted([b for b in CAMPUS_GRAPH.keys() if b in BUILDING_LAYOUT])

        tk.Label(top_frame, text="Start Building:").grid(row=0, column=0, padx=5, pady=5)
        self.start_var = tk.StringVar(value="CS")
        self.start_combo = ttk.Combobox(
            top_frame,
            textvariable=self.start_var,
            values=buildings,
            width=20,
            state="readonly"
        )
        self.start_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="End Building:").grid(row=0, column=2, padx=5, pady=5)
        self.end_var = tk.StringVar(value="TSU")
        self.end_combo = ttk.Combobox(
            top_frame,
            textvariable=self.end_var,
            values=buildings,
            width=20,
            state="readonly"
        )
        self.end_combo.grid(row=0, column=3, padx=5, pady=5)

        button_frame = tk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(button_frame, text="Run BFS", width=15, command=self.run_bfs).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Run DFS", width=15, command=self.run_dfs).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Run Dijkstra", width=15, command=self.run_dijkstra).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Run Prim MST", width=15, command=self.run_prim).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Clear", width=15, command=self.clear_all).grid(row=0, column=4, padx=5)

        middle_frame = tk.Frame(self.frame)
        middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(middle_frame, width=850, height=720, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.output_text = tk.Text(middle_frame, width=40, font=("Courier New", 10))
        self.output_text.pack(side="right", fill="y", padx=10)

        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")
        self.building_items.clear()
        self.path_items.clear()

        self.canvas.create_text(
            425, 25,
            text="CSUF Campus Block Map",
            font=("Arial", 14, "bold")
        )

        for building, (x1, y1, x2, y2) in BUILDING_LAYOUT.items():
            y1 += self.map_y_offset
            y2 += self.map_y_offset

            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#d9e8fb",
                outline="black",
                width=2
            )
            text_id = self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=building,
                font=("Arial", 10, "bold")
            )
            self.building_items[building] = (rect_id, text_id)

    def get_center(self, building):
        if building not in BUILDING_LAYOUT:
            return None

        x1, y1, x2, y2 = BUILDING_LAYOUT[building]
        y1 += self.map_y_offset
        y2 += self.map_y_offset

        return (x1 + x2) / 2, (y1 + y2) / 2

    def clear_path_visuals(self):
        for item in self.path_items:
            self.canvas.delete(item)
        self.path_items.clear()

        for building, (rect_id, _) in self.building_items.items():
            self.canvas.itemconfig(rect_id, fill="#d9e8fb", outline="black", width=2)

    def highlight_path(self, path, color="red"):
        self.clear_path_visuals()

        if not path:
            return

        visible_path = [building for building in path if building in BUILDING_LAYOUT]

        if not visible_path:
            return

        for i, building in enumerate(visible_path):
            rect_id, _ = self.building_items[building]

            if i == 0:
                self.canvas.itemconfig(rect_id, fill="#90ee90")   # start
            elif i == len(visible_path) - 1:
                self.canvas.itemconfig(rect_id, fill="#ffcccb")   # end
            else:
                self.canvas.itemconfig(rect_id, fill="#ffe699")   # middle

        for i in range(len(visible_path) - 1):
            x1, y1 = self.get_center(visible_path[i])
            x2, y2 = self.get_center(visible_path[i + 1])

            line_id = self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=4,
                arrow=tk.LAST
            )
            self.path_items.append(line_id)

    def write_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def clear_all(self):
        self.clear_output()
        self.draw_map()

    def get_start_end(self):
        start = self.start_var.get()
        end = self.end_var.get()

        if start not in BUILDING_LAYOUT or end not in BUILDING_LAYOUT:
            messagebox.showerror("Map Error", "Selected buildings are not available in the block map.")
            return None, None

        return start, end

    def run_bfs(self):
        start, end = self.get_start_end()
        if not start:
            return

        path = bfs_path(CAMPUS_GRAPH, start, end)

        self.clear_output()
        self.write_output("BFS RESULT")
        self.write_output("-" * 50)

        if path:
            self.write_output(f"Start: {start}")
            self.write_output(f"End: {end}")
            self.write_output(f"Path: {' -> '.join(path)}")
            self.write_output(f"Hops: {len(path) - 1}")
            self.highlight_path(path, color="blue")
        else:
            self.write_output("No BFS path found.")

    def run_dfs(self):
        start, end = self.get_start_end()
        if not start:
            return

        connected, order = is_connected_to(CAMPUS_GRAPH, start, end)

        self.clear_output()
        self.write_output("DFS + CONNECTIVITY RESULT")
        self.write_output("-" * 50)
        self.write_output(f"Start: {start}")
        self.write_output(f"End: {end}")
        self.write_output(f"Connected: {connected}")
        self.write_output("DFS Order:")
        self.write_output(" -> ".join(order))

        if connected:
            # DFS는 path가 아니라 traversal order라서
            # 필요하면 end까지 부분만 따로 강조 가능
            if end in order:
                idx = order.index(end)
                partial_path = order[:idx + 1]
                existing = [b for b in partial_path if b in BUILDING_LAYOUT]
                if len(existing) >= 2:
                    self.highlight_path(existing, color="purple")

    def run_dijkstra(self):
        start, end = self.get_start_end()
        if not start:
            return

        path, distance = dijkstra_shortest_path(CAMPUS_GRAPH, start, end)

        self.clear_output()
        self.write_output("DIJKSTRA RESULT")
        self.write_output("-" * 50)

        if path:
            self.write_output(f"Start: {start}")
            self.write_output(f"End: {end}")
            self.write_output(f"Shortest Path: {' -> '.join(path)}")
            self.write_output(f"Total Cost: {distance}")
            self.highlight_path(path, color="red")
        else:
            self.write_output("No Dijkstra path found.")

    def run_prim(self):
        start, _ = self.get_start_end()
        if not start:
            return

        mst_edges, total_weight = prim_mst(CAMPUS_GRAPH, start)

        self.clear_output()
        self.write_output("PRIM MST RESULT")
        self.write_output("-" * 50)
        self.write_output(f"Start Node: {start}")
        self.write_output(f"Total MST Weight: {total_weight}")
        self.write_output("Edges:")

        self.clear_path_visuals()

        for a, b, w in mst_edges:
            self.write_output(f"{a} -- {b} (weight={w})")

            if a in BUILDING_LAYOUT and b in BUILDING_LAYOUT:
                x1, y1 = self.get_center(a)
                x2, y2 = self.get_center(b)

                line_id = self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill="green",
                    width=2
                )
                self.path_items.append(line_id)