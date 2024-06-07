import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Выбор псевдонима
nickname = input("Choose your nickname: ")

# Подключение к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Функция для получения сообщений от сервера
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))  # Отправка псевдонима серверу
            else:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + '\n')  # Отображение сообщения в текстовом поле
                text_area.config(state=tk.DISABLED)
                text_area.see(tk.END)
        except:
            print("An error occurred!")
            client.close()
            break

# Функция для отправки сообщений на сервер
def write():
    message = f'{nickname}: {input_field.get()}'
    client.send(message.encode('utf-8'))  # Отправка сообщения
    input_field.delete(0, tk.END)  # Очистка поля ввода
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, message + '\n')  # Отображение отправленного сообщения
    text_area.config(state=tk.DISABLED)
    text_area.see(tk.END)

# Функция для добавления эмодзи в поле ввода
def send_emoji(emoji):
    input_field.insert(tk.END, emoji)

# Настройка графического интерфейса
root = tk.Tk()
root.title("Chat Client")

# Настройка текстового поля с прокруткой
frame = tk.Frame(root)
scrollbar = tk.Scrollbar(frame)
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame.pack(padx=10, pady=10)

# Настройка поля ввода и кнопки отправки
input_frame = tk.Frame(root)
input_field = tk.Entry(input_frame, width=50)
send_button = tk.Button(input_frame, text="Send", command=write)
input_field.pack(side=tk.LEFT, padx=5)
send_button.pack(side=tk.RIGHT)
input_frame.pack(padx=10, pady=10)

# Настройка кнопок для отправки эмодзи
emoji_frame = tk.Frame(root)
emojis = ['😊', '😂', '❤️', '👍', '🙌']
for emoji in emojis:
    button = tk.Button(emoji_frame, text=emoji, command=lambda e=emoji: send_emoji(e))
    button.pack(side=tk.LEFT, padx=5)
emoji_frame.pack(padx=10, pady=10)

# Запуск потоков для прослушивания и отправки сообщений
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
