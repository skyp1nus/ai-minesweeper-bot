import tkinter as tk

from game import play_minesweeper

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

def close_window():
    root.destroy()

def start_bot():
    play_minesweeper(root)

# Створюємо головне вікно
root = tk.Tk()
root.title("Область знімка екрану")
root.overrideredirect(True)  # Вимикаємо рамку вікна
root.attributes('-alpha', 1)  # Встановлюємо прозорість

# Налаштовуємо мінімальний розмір вікна
root.minsize(250, 200)

# Висота верхньої панелі
title_bar_height = 30

# Створюємо верхню панель
title_bar = tk.Frame(root, bg='gray', relief='raised', height=title_bar_height)
title_bar.pack(side=tk.TOP, fill=tk.X)

# Додаємо кнопку "Закрити" у верхній правий кут
close_button = tk.Button(title_bar, text='✕', command=close_window, bg='red', fg='white', bd=0, padx=5, pady=0)
close_button.pack(side=tk.RIGHT)

# Створюємо кнопку для знімка екрану
screenshot_button = tk.Button(root, text="Запустити", command=start_bot)
screenshot_button.pack(side=tk.BOTTOM, fill=tk.X)

# Додаємо можливість переміщення вікна
root.bind('<Button-1>', start_move)
root.bind('<B1-Motion>', do_move)

# Запускаємо головний цикл програми
root.mainloop()
