import tkinter as tk
from tkinter import scrolledtext
import shlex
import getpass
import socket
import argparse
import sys
import os


def get_system_info_title():
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"Эмулятор - [{username}@{hostname}]"


def parse_and_execute_command(command_str):
    """Обрабатывает одну команду и возвращает строку результата или 'exit'."""
    if not command_str.strip():
        return None  # Ничего не возвращать для пустых строк

    try:
        tokens = shlex.split(command_str)
    except ValueError as e:
        return f"shell: syntax error: {str(e)}"

    cmd = tokens[0]

    if cmd == "exit":
        return "exit"

    if cmd == "ls":
        args_str = ' '.join(tokens[1:]) if len(tokens) > 1 else ""
        return f"ls called with args: {args_str}" if args_str else "ls called with no arguments"

    if cmd == "cd":
        args_str = ' '.join(tokens[1:]) if len(tokens) > 1 else ""
        return f"cd called with args: {args_str}" if args_str else "cd called with no arguments"

    return f"{cmd}: command not found"


def execute_command_in_gui(command_str, output_widget, entry_widget=None):
    """Выполняет команду и выводит результат в GUI, как при ручном вводе."""
    result = parse_and_execute_command(command_str)

    output_widget.insert(tk.END, f"vfs$ {command_str}\n")

    if result == "exit":
        output_widget.insert(tk.END, "Выход из эмулятора...\n")
        output_widget.see(tk.END)
        output_widget.update()
        output_widget.master.after(500, output_widget.master.quit)
        return True  # сигнал завершения

    if result is not None:
        output_widget.insert(tk.END, f"{result}\n")

    output_widget.see(tk.END)
    if entry_widget:
        entry_widget.delete(0, tk.END)
    return False  # не выход


def run_script(script_path, output_widget):
    """Выполняет команды из скрипта построчно."""
    if not os.path.isfile(script_path):
        output_widget.insert(tk.END, f"Ошибка: скрипт не найден: {script_path}\n")
        return

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        output_widget.insert(tk.END, f"Ошибка чтения скрипта: {e}\n")
        return

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Пропускаем пустые строки и комментарии
        if execute_command_in_gui(line, output_widget):
            break  # exit был вызван


def main():
    parser = argparse.ArgumentParser(description="Эмулятор shell с поддержкой VFS и скриптов.")
    parser.add_argument("--vfs", type=str, help="Путь к физическому расположению VFS (заглушка)")
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту для выполнения")

    args = parser.parse_args()

    # Отладочный вывод параметров
    print("=== Отладочный вывод параметров запуска ===")
    print(f"VFS path: {args.vfs if args.vfs else 'не задан'}")
    print(f"Script path: {args.script if args.script else 'не задан'}")
    print("============================================\n")

    # Создание GUI
    root = tk.Tk()
    root.title(get_system_info_title())
    root.geometry("800x600")

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.NORMAL)
    output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(root)
    entry.pack(padx=10, pady=5, fill=tk.X)
    entry.bind("<Return>", lambda e: execute_command_in_gui(entry.get(), output_text, entry))

    send_button = tk.Button(
        root,
        text="Отправить",
        command=lambda: execute_command_in_gui(entry.get(), output_text, entry)
    )
    send_button.pack(pady=5)

    entry.focus_set()

    # Если задан скрипт — выполняем его после запуска GUI
    if args.script:
        # Используем after, чтобы запустить после инициализации GUI
        root.after(100, lambda: run_script(args.script, output_text))

    root.mainloop()


if __name__ == "__main__":
    main()
