import tkinter as tk
from tkinter import ttk, messagebox

from policy.fifo_policy import fifo
from policy.lru_policy import lru
from policy.mru_policy import mru
from policy.optimal_policy import optimal
from policy.second_chance_policy import second_chance


class PageReplacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.geometry("1000x900")
        self.root.resizable(True, True)

        self.sequence = []

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#0f172a", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Page Replacement Simulator", 
                 font=("Helvetica", 24, "bold"), fg="white", bg="#0f172a").pack(side="left", padx=30, pady=20)
        tk.Label(header, text="FIFO | LRU | MRU | Optimal | Second Chance", 
                 font=("Helvetica", 12), fg="#94a3b8", bg="#0f172a").pack(side="right", padx=30)

        # MAIN 
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Left Panel for inputs
        left_panel = tk.Frame(main_frame, width=340)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)

        # Algorithm Selection
        tk.Label(left_panel, text="Algorithm", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.algo_var = tk.StringVar(value="fifo")
        algo_combo = ttk.Combobox(left_panel, textvariable=self.algo_var, state="readonly")
        algo_combo['values'] = [
            "FIFO (First In First Out)",
            "LRU (Least Recently Used)",
            "MRU (Most Recently Used)",
            "Optimal",
            "Second Chance (Clock)"
        ]
        algo_combo.pack(fill="x", pady=(0, 15))

        # Number of Frames
        tk.Label(left_panel, text="Number of Frames", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(10, 5))
        self.frames_var = tk.IntVar(value=4)
        frames_spin = tk.Spinbox(left_panel, from_=1, to=20, textvariable=self.frames_var, 
                                font=("Helvetica", 16), width=10)
        frames_spin.pack(anchor="w", pady=(0, 20))

        # SEQUENCE INPUT
        tk.Label(left_panel, text="Page Request Sequence", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))
        
        # Count label
        self.seq_count_label = tk.Label(left_panel, text="0 requests", 
                                       font=("Helvetica", 11, "bold"), fg="#2563eb")
        self.seq_count_label.pack(anchor="e", pady=(0, 8))

        # Text area for pasting full sequence
        self.sequence_text = tk.Text(left_panel, height=6, font=("Consolas", 13), fg="gray")
        self.sequence_text.pack(fill="x", pady=(0, 10))
        self.sequence_text.insert("1.0", "Paste sequence here (e.g. 6 1 2 3 1 4 ... or 6,1,2,3...)")

        # Load Sequence Button
        tk.Button(left_panel, text="Load Sequence", command=self.load_sequence,
                  bg="#2563eb", fg="white", font=("Helvetica", 11, "bold")).pack(fill="x", pady=(0, 15))

        # Quick Add
        quick_frame = tk.Frame(left_panel)
        quick_frame.pack(fill="x", pady=(0, 10))
        tk.Label(quick_frame, text="Quick Add:", font=("Helvetica", 10)).pack(side="left")
        self.quick_entry = tk.Entry(quick_frame, font=("Helvetica", 13), width=15)
        self.quick_entry.pack(side="left", padx=8)
        self.quick_entry.bind("<Return>", lambda e: self.quick_add())
        tk.Button(quick_frame, text="Add", command=self.quick_add, 
                  bg="#22c55e", fg="black").pack(side="left")

        # Sequence List 
        tk.Label(left_panel, text="Current Sequence:", font=("Helvetica", 11)).pack(anchor="w", pady=(10, 5))
        self.seq_listbox = tk.Listbox(left_panel, font=("Consolas", 12), height=10)
        self.seq_listbox.pack(fill="both", expand=True, pady=(0, 10))

        # Control Buttons
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Clear Sequence", command=self.clear_sequence,
                  bg="#ef4444", fg="white").pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(btn_frame, text="RUN SIMULATION", command=self.run_simulation,
                  font=("Helvetica", 14, "bold"), bg="#22c55e", fg="black", height=2).pack(side="right", fill="x", expand=True)

        # RIGHT PANEL OUTPUT
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True)

        self.result_label = tk.Label(right_panel, text="Simulation Output", 
                                    font=("Helvetica", 16, "bold"))
        self.result_label.pack(anchor="w", pady=(0, 10))

        self.tree = ttk.Treeview(right_panel, show="headings")
        self.tree.pack(fill="both", expand=True, pady=(0, 15))

        vsb = ttk.Scrollbar(right_panel, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(right_panel, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.stats_frame = tk.Frame(right_panel)
        self.stats_frame.pack(fill="x")

        self.empty_label = tk.Label(right_panel, text="Load a sequence on the left\nthen run simulation", 
                                   font=("Helvetica", 14), fg="gray", justify="center")
        self.empty_label.pack(expand=True)

    def load_sequence(self):
        text = self.sequence_text.get("1.0", tk.END).strip()
        if not text or text == "Paste sequence here (e.g. 6 1 2 3 1 4 ... or 6,1,2,3...)":
            messagebox.showwarning("Empty", "Please enter or paste a sequence")
            return

        # Clean and split the input (handles spaces, commas, mixed)
        cleaned = text.replace(",", " ").replace("  ", " ")
        tokens = cleaned.split()

        new_sequence = []
        for token in tokens:
            token = token.strip()
            if token:
                try:
                    page = int(token) if token.isdigit() else token
                    new_sequence.append(page)
                except:
                    continue

        if not new_sequence:
            messagebox.showerror("Invalid", "No valid pages found in input")
            return

        self.sequence = new_sequence
        self.refresh_sequence_list()
        messagebox.showinfo("Success", f"Loaded {len(self.sequence)} page requests")

    def quick_add(self):
        text = self.quick_entry.get().strip()
        if not text:
            return
        try:
            page = int(text) if text.isdigit() else text
            self.sequence.append(page)
            self.refresh_sequence_list()
            self.quick_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Invalid", "Enter a valid page")

    def refresh_sequence_list(self):
        self.seq_listbox.delete(0, tk.END)
        for i, page in enumerate(self.sequence):
            self.seq_listbox.insert(tk.END, f"{i+1:2d}. {page}")

        self.seq_count_label.config(text=f"{len(self.sequence)} requests")

    def clear_sequence(self):
        self.sequence.clear()
        self.refresh_sequence_list()

    def run_simulation(self):
        if not self.sequence:
            messagebox.showwarning("Empty Sequence", "Please load or add page requests first.")
            return

        capacity = self.frames_var.get()
        algo_name = self.algo_var.get()

        algo_map = {
            "FIFO (First In First Out)": fifo,
            "LRU (Least Recently Used)": lru,
            "MRU (Most Recently Used)": mru,
            "Optimal": optimal,
            "Second Chance (Clock)": second_chance
        }

        func = algo_map.get(algo_name)
        if not func:
            messagebox.showerror("Error", "Algorithm not found")
            return

        try:
            result = func(self.sequence, len(self.sequence), capacity)
            self.display_results(result, algo_name)
        except Exception as e:
            messagebox.showerror("Simulation Error", str(e))

    def display_results(self, result, algo_name):
        self.empty_label.pack_forget()

        self.result_label.config(text=f"{algo_name} • {len(self.sequence)} Requests • {result['capacity']} Frames")

        # Clear old table
        for item in self.tree.get_children():
            self.tree.delete(item)

        cols = ["Frame"] + [str(p) for p in result['pages']]
        self.tree["columns"] = cols
        self.tree["show"] = "headings"

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=65, anchor="center")

        # Frame rows
        for i in range(result['capacity']):
            row = [f"F{i}"] + [str(x) if x != '' else '—' for x in result['frame_history'][i]]
            self.tree.insert("", "end", values=row)

        # PI row
        pi_row = ["PI"] + result['fault_history']
        self.tree.insert("", "end", values=pi_row, tags=("pi",))
        self.tree.tag_configure("pi", background="#fee2e2", foreground="#b91c1c")

        # Stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        stats = [
            ("Page Faults", result['page_faults'], "#dc2626"),
            ("Page Hits", result['page_hits'], "#16a34a"),
            ("Failure Rate", f"{result['failure_rate']:.2f}%", "#dc2626"),
            ("Success Rate", f"{result['success_rate']:.2f}%", "#16a34a")
        ]

        for label, value, color in stats:
            frame = tk.Frame(self.stats_frame, relief="solid", borderwidth=1)
            frame.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(frame, text=label, font=("Helvetica", 10)).pack(pady=(8, 2))
            tk.Label(frame, text=str(value), font=("Helvetica", 18, "bold"), fg=color).pack(pady=(0, 8))


if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementGUI(root)
    root.mainloop()