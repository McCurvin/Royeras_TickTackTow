import tkinter as tk
import tkinter.messagebox as messagebox
from datetime import datetime

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")
        master.configure(bg='black')
        self.tasks = {}

        self.task_entry = tk.Text(master, width=40, height=5, bg='black', fg='white')
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.date_label = tk.Label(master, text="Date (YYYY-MM-DD):", bg='black', fg='white')
        self.date_label.grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(master, width=15, bg='black', fg='white')
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Set default date to current date

        self.add_button = tk.Button(master, text="Add Tasks", command=self.add_tasks, bg='black', fg='white')
        self.add_button.grid(row=1, column=2, padx=5, pady=5)

        self.task_listbox = tk.Listbox(master, width=50, bg='black', fg='white')
        self.task_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.complete_button = tk.Button(master, text="Mark as Complete", command=self.mark_as_complete, bg='black', fg='white')
        self.complete_button.grid(row=2, column=2, padx=5, pady=5)

        self.clear_button = tk.Button(master, text="Clear Tasks", command=self.clear_tasks, bg='black', fg='white')
        self.clear_button.grid(row=3, column=0, padx=5, pady=5)

        self.save_button = tk.Button(master, text="Save Tasks", command=self.save_tasks, bg='black', fg='white')
        self.save_button.grid(row=3, column=1, padx=5, pady=5)

    def add_tasks(self):
        tasks = self.task_entry.get("1.0", tk.END).splitlines()
        date = self.date_entry.get()
        if not all(tasks):
            messagebox.showwarning("Warning", "Please enter tasks.")
        else:
            if date:
                tasks_with_date = [f"{date}: {task}" for task in tasks]
                if date not in self.tasks:
                    self.tasks[date] = []
                self.tasks[date].extend(tasks_with_date)  # Append new tasks to existing tasks for the date
                self.update_task_listbox(date)  # Update the task listbox with the updated tasks
                self.task_entry.delete("1.0", tk.END)
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Reset date to current date
            else:
                messagebox.showwarning("Warning", "Please enter a date for the tasks.")

    def update_task_listbox(self, date):
        if date in self.tasks:
            self.task_listbox.delete(0, tk.END)
            for task in self.tasks[date]:
                self.task_listbox.insert(tk.END, task)
        else:
            messagebox.showwarning("Warning", f"No tasks found for {date}.")

    def mark_as_complete(self):
        selected_indices = self.task_listbox.curselection()
        if selected_indices:
            for index in selected_indices:
                task = self.task_listbox.get(index)
                if " [DONE]" not in task:
                    self.task_listbox.delete(index)
                    self.task_listbox.insert(index, task + " [DONE]")

    def clear_tasks(self):
        date = self.date_entry.get()
        if date:
            if date in self.tasks:
                del self.tasks[date]
                self.task_listbox.delete(0, tk.END)
                messagebox.showinfo("Information", f"Tasks for {date} cleared.")
            else:
                messagebox.showwarning("Warning", f"No tasks found for {date}.")
        else:
            messagebox.showwarning("Warning", "Please enter a date.")

    def save_tasks(self):
        filename = "tasks.txt"
        with open(filename, "a") as file:  # Open file in append mode to append taskss
            for date, tasks in self.tasks.items():
                file.write(f"Date: {date}\n")
                for task in tasks:
                    file.write(f"{task}\n")
                file.write("\n")
        messagebox.showinfo("Information", f"Tasks saved to {filename}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
