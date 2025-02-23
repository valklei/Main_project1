import tkinter as tk
from tkinter import messagebox, ttk
from add_and_update_created_db import *

class FilmSearchApp:
    def __init__(self, root, query_handler):
        self.root = root
        self.query_handler = query_handler
        self.current_frame = None  # Инициализация current_frame
        self.create_tables()
        self.create_widgets()

    def create_tables(self):
        # Создание таблиц в базе данных
        create_tables()

    def create_widgets(self):
        # Настройка основного окна
        self.root.title("Film Search")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Основной фрейм для навигации
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для кнопок навигации
        self.nav_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Кнопки навигации
        self.genres_button = tk.Button(self.nav_frame, text="Поиск по жанрам", command=self.show_genres_frame, font=("Arial", 12), width=20)
        self.genres_button.pack(pady=5)

        self.keyword_button = tk.Button(self.nav_frame, text="Поиск по ключевому слову", command=self.show_keyword_frame, font=("Arial", 12), width=20)
        self.keyword_button.pack(pady=5)

        self.searched_button = tk.Button(self.nav_frame, text="Самые частые запросы", command=self.show_searched_frame, font=("Arial", 12), width=20)
        self.searched_button.pack(pady=5)

        self.exit_button = tk.Button(self.nav_frame, text="Выход", command=self.exit_app, font=("Arial", 12), width=20)
        self.exit_button.pack(pady=5)

        # Фрейм для отображения контента
        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Инициализация фреймов для каждого окна
        self.genres_frame = ttk.Frame(self.content_frame)
        self.years_frame = ttk.Frame(self.content_frame)
        self.keyword_frame = ttk.Frame(self.content_frame)
        self.searched_frame = ttk.Frame(self.content_frame)

        # Начальное отображение фрейма поиска по жанрам
        self.show_genres_frame()

    def show_genres_frame(self):
        self.hide_current_frame()
        self.current_frame = self.genres_frame
        self.genres_frame.pack(fill=tk.BOTH, expand=True)

        # Очистка фрейма перед добавлением новых виджетов
        for widget in self.genres_frame.winfo_children():
            widget.destroy()

        # Получение всех жанров
        genres = self.query_handler.get_all_category()
        if not genres:
            messagebox.showinfo("Информация", "Жанры не найдены.")
            return

        # Метка для доступных жанров
        genre_label = tk.Label(self.genres_frame, text="Доступные жанры:", font=("Arial", 12), bg="#f0f0f0")
        genre_label.pack(pady=10)

        # Переменная для хранения выбранного жанра
        self.genre_var = tk.StringVar()
        for genre in genres:
            genre_radio = tk.Radiobutton(self.genres_frame, text=genre, variable=self.genre_var, value=genre, font=("Arial", 10), bg="#f0f0f0")
            genre_radio.pack(anchor=tk.W)

        # Кнопка для подтверждения выбора жанра
        genre_submit_button = tk.Button(self.genres_frame, text="Подтвердить жанр", command=self.confirm_genre_selection, font=("Arial", 12))
        genre_submit_button.pack(pady=10)

    def confirm_genre_selection(self):
        genre = self.genre_var.get()
        if not genre:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите жанр.")
            return
        self.show_years_frame(genre)

    def show_years_frame(self, genre):
        self.hide_current_frame()
        self.current_frame = self.years_frame
        self.years_frame.pack(fill=tk.BOTH, expand=True)

        # Очистка фрейма перед добавлением новых виджетов
        for widget in self.years_frame.winfo_children():
            widget.destroy()

        # Метка для выбранного жанра
        selected_genre_label = tk.Label(self.years_frame, text=f"Выбранный жанр: {genre}", font=("Arial", 12), bg="#f0f0f0")
        selected_genre_label.pack(pady=10)

        # Получение всех годов
        years = self.query_handler.get_all_year()

        # Метка для доступных годов
        year_label = tk.Label(self.years_frame, text="Доступные года:", font=("Arial", 12), bg="#f0f0f0")
        year_label.pack(pady=10)

        # Фрейм для списка годов
        years_list_frame = tk.Frame(self.years_frame, bg="#f0f0f0")
        years_list_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas для списка годов
        canvas = tk.Canvas(years_list_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(years_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Переменная для хранения выбранного года
        self.year_var = tk.StringVar()
        for year in years:
            year_radio = tk.Radiobutton(scrollable_frame, text=f'Год выпуска: {year}', variable=self.year_var, value=year, font=("Arial", 10), bg="#f0f0f0")
            year_radio.pack(anchor=tk.W)

        # Кнопка для подтверждения выбора года
        year_submit_button = tk.Button(self.years_frame, text="Подтвердить год", command=lambda: self.search_by_genre_and_year(genre), font=("Arial", 12))
        year_submit_button.pack(pady=10)

    def search_by_genre_and_year(self, genre):
        year = self.year_var.get()
        if not year:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите год.")
            return

        if not year.isdigit() or int(year) < 1901 or int(year) > 2155:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный год.")
            return

        # Обновление счетчика запросов по жанру и году
        add_or_update_count_genre_year(genre, int(year))
        result_gen = self.query_handler.get_film_by_category_and_year(genre, int(year))

        if result_gen:
            self.show_results(result_gen, f"Результат поиска по жанру: {genre} и году выпуска: {year}")
        else:
            messagebox.showinfo("Информация", "Фильмы не найдены.")

    def show_keyword_frame(self):
        self.hide_current_frame()
        self.current_frame = self.keyword_frame
        self.keyword_frame.pack(fill=tk.BOTH, expand=True)

        # Очистка фрейма перед добавлением новых виджетов
        for widget in self.keyword_frame.winfo_children():
            widget.destroy()

        # Метка для ввода ключевого слова
        keyword_label = tk.Label(self.keyword_frame, text="Введите слово для поиска:", font=("Arial", 12), bg="#f0f0f0")
        keyword_label.pack(pady=10)

        # Поле для ввода ключевого слова
        keyword_entry = tk.Entry(self.keyword_frame, font=("Arial", 12), width=25)
        keyword_entry.pack(pady=5)

        # Кнопка для поиска по ключевому слову
        submit_button = tk.Button(self.keyword_frame, text="Поиск", command=lambda: self.search_by_keyword(keyword_entry.get()), font=("Arial", 12))
        submit_button.pack(pady=10)

    def search_by_keyword(self, keyword):
        # Обновление счетчика запросов по ключевому слову
        add_or_update_count_keywords(keyword)
        result_kw = self.query_handler.get_films_by_keyword(keyword)

        if result_kw:
            self.show_results(result_kw, f"Результат поиска по ключевому слову: {keyword}")
        else:
            messagebox.showinfo("Информация", "Фильмы не найдены.")

    def show_searched_frame(self):
        self.hide_current_frame()
        self.current_frame = self.searched_frame
        self.searched_frame.pack(fill=tk.BOTH, expand=True)

        # Очистка фрейма перед добавлением новых виджетов
        for widget in self.searched_frame.winfo_children():
            widget.destroy()

        # Получение самых частых запросов
        search_res_key = get_search_rating_keywords()
        search_res_gen = get_search_rating_genres()

        # Отображение результатов
        result_text = tk.Text(self.searched_frame, font=("Arial", 12), bg="#ffffff")
        result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        result_text.insert(tk.END, "Самые частые запросы по ключевому полю:\n")
        for res in search_res_key:
            result_text.insert(tk.END, f"Ключевое слово: {res[0]} -- Количество вводов: {res[1]}\n")

        result_text.insert(tk.END, "\nСамые частые запросы по жанру и году:\n")
        for res in search_res_gen:
            result_text.insert(tk.END, f"Жанр: {res[0]}, Год: {res[2]}, Количество вводов: {res[1]}\n")

        # Добавление скролла
        scrollbar = ttk.Scrollbar(self.searched_frame, orient="vertical", command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.configure(yscrollcommand=scrollbar.set)

    def show_results(self, results, title):
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("600x400")
        result_window.configure(bg="#f0f0f0")

        result_text = tk.Text(result_window, font=("Arial", 12), bg="#ffffff")
        result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        for item in results:
            if len(item) == 2:
                title, description = item
                result_text.insert(tk.END, f"Название: {title}\nОписание: {description}\n\n")
            elif len(item) == 3:
                title, release_year, description = item
                result_text.insert(tk.END, f"Название: {title}\nГод выпуска: {release_year}\nОписание: {description}\n\n")

        # Добавление скролла
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.configure(yscrollcommand=scrollbar.set)

    def hide_current_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()

    def exit_app(self):
        # Закрытие соединения с базой данных и завершение работы приложения
        self.query_handler.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    query_handler = QueryHandler()  # Предполагается, что QueryHandler инициализирует соединение с базой данных
    app = FilmSearchApp(root, query_handler)
    root.mainloop()
