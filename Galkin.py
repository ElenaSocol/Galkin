import tkinter as tk
from tkinter import ttk, messagebox
import json

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Movie Library")
        self.root.geometry("750x550")
        
        self.movies = self.load_data()
        self.setup_ui()

    def setup_ui(self):
        # --- ФОРМА ВВОДА ---
        frame_input = tk.LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky="e")
        self.entry_title = tk.Entry(frame_input, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Жанр:").grid(row=0, column=2, sticky="e")
        self.combo_genre = ttk.Combobox(frame_input, values=["Боевик", "Комедия", "Драма", "Ужасы", "Фантастика", "Мультфильм"])
        self.combo_genre.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_input, text="Год:").grid(row=1, column=0, sticky="e")
        self.entry_year = tk.Entry(frame_input, width=30)
        self.entry_year.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="e")
        self.entry_rating = tk.Entry(frame_input)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=2)

        btn_add = tk.Button(frame_input, text="Добавить фильм", command=self.add_movie, bg="#2196F3", fg="white")
        btn_add.grid(row=2, column=0, columnspan=4, sticky="we", pady=10)

        # --- ФИЛЬТРЫ ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = ttk.Combobox(frame_filter, values=["Все"] + ["Боевик", "Комедия", "Драма", "Ужасы", "Фантастика", "Мультфильм"])
        self.filter_genre.set("Все")
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Год:").grid(row=0, column=2)
        self.filter_year = tk.Entry(frame_filter, width=10)
        self.filter_year.grid(row=0, column=3, padx=5)

        btn_apply = tk.Button(frame_filter, text="Применить фильтр", command=self.update_table)
        btn_apply.grid(row=0, column=4, padx=10)

        # --- ТАБЛИЦА ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.update_table()

    def add_movie(self):
        title = self.entry_title.get()
        genre = self.combo_genre.get()
        year = self.entry_year.get()
        rating = self.entry_rating.get()

        # Валидация
        try:
            year_int = int(year)
            rating_float = float(rating)
            if not (0 <= rating_float <= 10): raise ValueError
            if not title or not genre: raise IndexError
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом, а рейтинг — от 0 до 10")
            return
        except IndexError:
            messagebox.showwarning("Внимание", "Заполните название и выберите жанр")
            return

        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year_int,
            "rating": rating_float
        })
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        f_genre = self.filter_genre.get()
        f_year = self.filter_year.get()

        for m in self.movies:
            genre_match = (f_genre == "Все" or m["genre"] == f_genre)
            year_match = (not f_year or str(m["year"]) == f_year)

            if genre_match and year_match:
                self.tree.insert("", "end", values=(m["title"], m["genre"], m["year"], m["rating"]))

    def save_data(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("movies.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

if __name__ == "__main__":
    root = tk.Tk()
    MovieLibrary(root)
    root.mainloop()
