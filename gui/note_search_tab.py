"""
note_search_tab.py — TCAA Notes Search Engine
Provides NoteSearchTab, a ttk.Frame subclass that can be embedded in any
ttk.Notebook by a teammate.  All string-search logic is delegated to
algorithms/string_search.py; file loading is handled by utils/file_loader.py.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

from algorithms.string_search import naive_search, rabin_karp_search, kmp_search, compare_all
from utils.file_loader import load_file

# Maximum match indices shown before "...and N more" is printed
MAX_SHOWN_INDICES = 20
# Characters of context to show around the first match
CONTEXT_RADIUS = 50


class NoteSearchTab(ttk.Frame):
    """
    Drop-in Tkinter tab for the Notes Search Engine feature of TCAA.

    Usage (in main.py)::

        notebook = ttk.Notebook(root)
        tab = NoteSearchTab(notebook)
        notebook.add(tab, text="Notes Search")
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.document_text: str = ""   # full text of the loaded file
        self._loaded_path:  str = ""   # path shown in the UI label

        self._build_ui()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Construct every widget and place it on the grid."""
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        pad = {"padx": 8, "pady": 4}

        # Row 0 — title
        title_font = ("Helvetica", 16, "bold")
        ttk.Label(
            self, text="Notes Search Engine", font=title_font
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(12, 6))

        # Row 1 — file upload
        ttk.Label(self, text="Upload Document:").grid(row=1, column=0, sticky="w", **pad)

        self._file_label = ttk.Label(
            self, text="No file loaded", relief="sunken",
            width=55, anchor="w"
        )
        self._file_label.grid(row=1, column=1, sticky="ew", **pad)

        ttk.Button(
            self, text="Browse", command=self._browse_file
        ).grid(row=1, column=2, sticky="w", **pad)

        # Row 2 — pattern entry
        ttk.Label(self, text="Search Pattern:").grid(row=2, column=0, sticky="w", **pad)

        self._pattern_var = tk.StringVar()
        ttk.Entry(
            self, textvariable=self._pattern_var, width=40
        ).grid(row=2, column=1, sticky="ew", **pad)

        # Row 3 — algorithm selector
        ttk.Label(self, text="Algorithm:").grid(row=3, column=0, sticky="w", **pad)

        self._algo_var = tk.StringVar(value="ALL (Compare)")
        ttk.Combobox(
            self,
            textvariable=self._algo_var,
            values=["Naive", "Rabin-Karp", "KMP", "ALL (Compare)"],
            state="readonly",
            width=20,
        ).grid(row=3, column=1, sticky="w", **pad)

        # Row 4 — search button
        ttk.Button(
            self, text="Search", command=self._run_search,
        ).grid(row=4, column=0, columnspan=3, pady=(6, 4))

        # Row 5 — results label
        ttk.Label(self, text="Results:").grid(row=5, column=0, sticky="w", **pad)

        # Row 6 — scrollable results area
        self._results_box = scrolledtext.ScrolledText(
            self, height=20, width=80, wrap=tk.WORD,
            state="disabled", font=("Courier", 11),
        )
        self._results_box.grid(
            row=6, column=0, columnspan=3, sticky="nsew", padx=8, pady=(0, 8)
        )
        self.rowconfigure(6, weight=1)

    # ── Event handlers ─────────────────────────────────────────────────────────

    def _browse_file(self) -> None:
        """Open a file dialog and load the selected document."""
        path = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[
                ("Supported files", "*.pdf *.docx *.txt"),
                ("PDF files",       "*.pdf"),
                ("Word documents",  "*.docx"),
                ("Text files",      "*.txt"),
                ("All files",       "*.*"),
            ],
        )
        if not path:
            return  # user cancelled

        try:
            self.document_text = load_file(path)
            self._loaded_path   = path
            char_count = len(self.document_text)
            display    = f"{path.split('/')[-1]}  ({char_count:,} chars)"
            self._file_label.config(text=display)
            self._write_results(f"Loaded: {path}\nCharacters: {char_count:,}\n")
        except Exception as exc:
            messagebox.showerror("Load Error", str(exc))
            self.document_text = ""
            self._file_label.config(text="No file loaded")

    def _run_search(self) -> None:
        """Execute the selected search algorithm and display results."""
        if not self.document_text:
            messagebox.showwarning("No Document", "Please load a document first.")
            return

        pattern = self._pattern_var.get().strip()
        if not pattern:
            messagebox.showwarning("Empty Pattern", "Please enter a search pattern.")
            return

        algo = self._algo_var.get()

        try:
            if algo == "ALL (Compare)":
                output = self._format_comparison(self.document_text, pattern)
            else:
                output = self._format_single(self.document_text, pattern, algo)
        except Exception as exc:
            output = f"[ERROR] Search failed:\n{exc}"

        self._write_results(output)

    # ── Formatting helpers ─────────────────────────────────────────────────────

    def _format_single(self, text: str, pattern: str, algo: str) -> str:
        """Run one algorithm and return a formatted result string."""
        if algo == "Naive":
            matches, elapsed = naive_search(text, pattern)
        elif algo == "Rabin-Karp":
            matches, elapsed = rabin_karp_search(text, pattern)
        else:  # KMP
            matches, elapsed = kmp_search(text, pattern)

        lines = [
            f"Algorithm : {algo}",
            f"Pattern   : {pattern!r}",
            f"Matches   : {len(matches)}",
            f"Time      : {elapsed:.3f} ms",
            "",
        ]

        if matches:
            shown = matches[:MAX_SHOWN_INDICES]
            lines.append(f"Match indices: {shown}")
            if len(matches) > MAX_SHOWN_INDICES:
                lines.append(f"  ...and {len(matches) - MAX_SHOWN_INDICES} more matches")
            lines.append("")
            lines.append(self._context_snippet(text, pattern, matches[0]))
        else:
            lines.append("No matches found.")

        return "\n".join(lines)

    def _format_comparison(self, text: str, pattern: str) -> str:
        """Run all three algorithms and return a side-by-side comparison."""
        results = compare_all(text, pattern)

        col_w = 14  # width for each data column

        header = (
            f"{'Algorithm':<14} {'Matches':>{col_w}} {'Time (ms)':>{col_w}}\n"
            + "-" * (14 + col_w * 2 + 4)
        )

        rows = []
        for name in ("Naive", "Rabin-Karp", "KMP"):
            r = results[name]
            rows.append(
                f"{name:<14} {r['count']:>{col_w}} {r['time_ms']:>{col_w}.3f}"
            )

        # Agreement check
        counts  = [results[n]["count"]   for n in ("Naive", "Rabin-Karp", "KMP")]
        indices = [results[n]["matches"] for n in ("Naive", "Rabin-Karp", "KMP")]
        if len(set(counts)) == 1 and indices[0] == indices[1] == indices[2]:
            verdict = "✓ All algorithms agree on match count and positions."
        else:
            verdict = "✗ MISMATCH — check implementation!"

        lines = [
            f"Pattern : {pattern!r}",
            "",
            header,
            *rows,
            "",
            verdict,
        ]

        # Show context around first match (if any)
        first_matches = results["Naive"]["matches"]
        if first_matches:
            lines.append("")
            lines.append(self._context_snippet(text, pattern, first_matches[0]))

        return "\n".join(lines)

    @staticmethod
    def _context_snippet(text: str, pattern: str, index: int) -> str:
        """Return a formatted snippet showing context around a match."""
        start  = max(0, index - CONTEXT_RADIUS)
        end    = min(len(text), index + len(pattern) + CONTEXT_RADIUS)
        before = text[start:index]
        match  = text[index:index + len(pattern)]
        after  = text[index + len(pattern):end]

        ellipsis_l = "..." if start > 0  else ""
        ellipsis_r = "..." if end < len(text) else ""

        snippet = f'{ellipsis_l}{before}[[ {match} ]]{after}{ellipsis_r}'
        return f"Context around first match (index {index}):\n  {snippet}"

    # ── Utility ────────────────────────────────────────────────────────────────

    def _write_results(self, text: str) -> None:
        """Replace the contents of the results box with the given text."""
        self._results_box.config(state="normal")
        self._results_box.delete("1.0", tk.END)
        self._results_box.insert(tk.END, text)
        self._results_box.config(state="disabled")
