import tkinter as tk
from tkinter import filedialog
import os

def ask_open_filename(title, filetypes, initialdir=None):
    """
    Запускает Tkinter-файлдиалог и возвращает путь к файлу.
    Если initialdir пустой или None, берётся os.getcwd().
    """
    # Создаём и прячем корневое окно
    root = tk.Tk()
    root.withdraw()

    # Если не задана папка — по умолчанию текущая
    if not initialdir:
        initialdir = os.getcwd()

    path = filedialog.askopenfilename(
        parent=root,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes
    )

    # Уничтожаем корень сразу же
    root.destroy()

    # Если пользователь нажал Cancel — возвращаем пустую строку
    return path or ""
