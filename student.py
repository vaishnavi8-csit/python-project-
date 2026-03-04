import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def get_average(self):
        if self.scores:
            return np.mean(self.scores)
        return 0

    def get_median(self):
        if self.scores:
            return np.median(self.scores)
        return 0

    def get_std_dev(self):
        if self.scores:
            return np.std(self.scores)
        return 0


class StudentPerformanceAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Performance Analyzer")
        self.geometry("700x500")

        self.students = {}

        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = ttk.Frame(self)
        input_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, sticky='w')
        self.entry_id = ttk.Entry(input_frame)
        self.entry_id.grid(row=0, column=1, sticky='w')

        ttk.Label(input_frame, text="Student Name:").grid(row=1, column=0, sticky='w')
        self.entry_name = ttk.Entry(input_frame)
        self.entry_name.grid(row=1, column=1, sticky='w')

        ttk.Label(input_frame, text="Score:").grid(row=2, column=0, sticky='w')
        self.entry_score = ttk.Entry(input_frame)
        self.entry_score.grid(row=2, column=1, sticky='w')

        ttk.Button(input_frame, text="Add/Update Student Score", command=self.add_update_student).grid(row=3, column=0, columnspan=2, pady=5)

        # Student List
        list_frame = ttk.Frame(self)
        list_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.student_list = tk.Listbox(list_frame)
        self.student_list.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.student_list.yview)
        scrollbar.pack(side='right', fill='y')
        self.student_list.config(yscrollcommand=scrollbar.set)

        self.student_list.bind('<<ListboxSelect>>', self.show_statistics)

        # Stats Frame
        stats_frame = ttk.Frame(self)
        stats_frame.pack(padx=10, pady=10, fill='x')

        self.label_avg = ttk.Label(stats_frame, text="Average: N/A")
        self.label_avg.pack(anchor='w')

        self.label_median = ttk.Label(stats_frame, text="Median: N/A")
        self.label_median.pack(anchor='w')

        self.label_std = ttk.Label(stats_frame, text="Standard Deviation: N/A")
        self.label_std.pack(anchor='w')

        # Plot Frame
        plot_frame = ttk.Frame(self)
        plot_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.figure = plt.Figure(figsize=(6, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.chart = FigureCanvasTkAgg(self.figure, plot_frame)
        self.chart.get_tk_widget().pack(fill='both', expand=True)

    def add_update_student(self):
        student_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        score_text = self.entry_score.get().strip()

        if not student_id or not name or not score_text:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            score = float(score_text)
        except ValueError:
            messagebox.showerror("Input Error", "Score must be a number.")
            return

        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        else:
            # Update name in case it changed
            self.students[student_id].name = name

        self.students[student_id].add_score(score)
        self.update_student_list()
        self.clear_entries()

    def update_student_list(self):
        self.student_list.delete(0, tk.END)
        for student_id, student in self.students.items():
            display_text = f"{student_id} - {student.name} (Scores: {len(student.scores)})"
            self.student_list.insert(tk.END, display_text)

    def clear_entries(self):
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_score.delete(0, tk.END)

    def show_statistics(self, event):
        if not self.student_list.curselection():
            return
        index = self.student_list.curselection()[0]
        student_key = list(self.students.keys())[index]
        student = self.students[student_key]

        avg = student.get_average()
        median = student.get_median()
        std = student.get_std_dev()

        self.label_avg.config(text=f"Average: {avg:.2f}")
        self.label_median.config(text=f"Median: {median:.2f}")
        self.label_std.config(text=f"Standard Deviation: {std:.2f}")

        self.plot_scores(student)

    def plot_scores(self, student):
        self.ax.clear()
        self.ax.plot(student.scores, marker='o', linestyle='-', color='blue')
        self.ax.set_title(f"Scores for {student.name}")
        self.ax.set_xlabel("Test Number")
        self.ax.set_ylabel("Score")
        self.ax.grid(True)
        self.figure.tight_layout()
        self.chart.draw()


if __name__ == "__main__":
    app = StudentPerformanceAnalyzerApp()
    app.mainloop()
