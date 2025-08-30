import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import os
from datetime import datetime

FILENAME = "weights.csv"

def load_data():
    if not os.path.exists(FILENAME):
        return [], []
    with open(FILENAME, "r", encoding="utf-8", newline="") as f:
        reader = list(csv.reader(f))
        if not reader:
            return [], []
        header = reader[0]
        rows = reader[1:]
        return header, rows

def save_data(header, rows):
    try:
        rows.sort(key=lambda r: datetime.strptime(r[0], "%Y-%m-%d"))
    except Exception:
        pass
    with open(FILENAME, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

class WeightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вес семьи (CSV)")
        
        self.header, self.rows = load_data()
        if not self.header:
            self.header = ["Дата", "Дима", "Света", "Максим", "Саша"]

        self.tree = ttk.Treeview(root, columns=self.header, show="headings")
        for col in self.header:
            self.tree.heading(col, text=col, command=lambda c=col: self.set_selected_person(c))
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        self.selected_person = None
        self.label = tk.Label(frame, text="Выбран: никто")
        self.label.grid(row=0, column=0, padx=5)

        tk.Button(frame, text="Добавить вес", command=self.add_weight).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Обновить таблицу", command=self.refresh_table).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Удалить запись", command=self.delete_record).grid(row=0, column=3, padx=5)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.rows:
            self.tree.insert("", "end", values=row)

    def set_selected_person(self, col):
        if col == "Дата":
            return
        self.selected_person = col
        self.label.config(text=f"Выбран: {col}")

    def add_weight(self):
        if not self.selected_person:
            messagebox.showwarning("Ошибка", "Сначала выберите человека (клик по имени в заголовке).")
            return

        weight = simpledialog.askfloat("Вес", f"Введите новый вес для {self.selected_person}:")
        if weight is None:
            return

        today = str(datetime.now().date())

        row = None
        for r in self.rows:
            if r[0] == today:
                row = r
                break

        if row is None:
            row = [today] + [""] * (len(self.header) - 1)
            self.rows.append(row)

        idx = self.header.index(self.selected_person)
        row[idx] = weight

        save_data(self.header, self.rows)
        self.refresh_table()
        messagebox.showinfo("Успех", f"Вес {self.selected_person} обновлён.")

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_idx = int(col.replace('#','')) - 1

        if col_idx == 0:
            return

        old_value = self.tree.item(item)["values"][col_idx]
        new_value = simpledialog.askstring("Изменить", f"Введите новое значение (было: {old_value}):")
        if new_value is not None:
            row_idx = self.tree.index(item)
            self.rows[row_idx][col_idx] = new_value
            save_data(self.header, self.rows)
            self.refresh_table()

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления.")
            return

        row_idx = self.tree.index(selected_item[0])
        date = self.rows[row_idx][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить запись за {date}?"):
            self.rows.pop(row_idx)
            save_data(self.header, self.rows)
            self.refresh_table()
            messagebox.showinfo("Успех", f"Запись за {date} удалена.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeightApp(root)
    root.mainloop()
