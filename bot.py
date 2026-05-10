import telebot
from flask import Flask
import threading
import socket

TOKEN = '8737751023:AAGjcTZIADQ86f3AyURHq0KiP5X4UocX4a0'
ADMIN_ID = 8648741496
RCON_HOST = 'localhost'
RCON_PORT = 25575
RCON_PASS = 'GrifMC_Admin_2026'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def rcon_cmd(command):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((RCON_HOST, RCON_PORT))
        # Логинимся
        sock.send(b'\x00\x00\x00\x00' + RCON_PASS.encode() + b'\x00')
        sock.recv(1024)
        # Отправляем команду
        sock.send(b'\x00\x00\x00\x00' + command.encode() + b'\x00')
        response = sock.recv(4096).decode('utf-8', errors='ignore')
        sock.close()
        return response.strip() if response.strip() else "✅ Выполнено"
    except Exception as e:
        return f"❌ Ошибка: {e}"

@app.route('/')
def home():
    return "RCON Bot работает!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        "🛠️ GrifMC RCON Бот\n"
        "!rcon tps\n"
        "!rcon list\n"
        "!rcon say текст\n"
        "!rcon команда"
    )

@bot.message_handler(func=lambda m: True)
def handle_rcon(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Только админ!")
        return
    
    text = message.text.strip()
    if not text.startswith('!rcon '):
        bot.send_message(message.chat.id, "Используй `!rcon команда`")
        return
    
    command = text[6:].strip()
    response = rcon_cmd(command)
    if len(response) > 4000:
        response = response[:3900] + "..."
    
    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.polling(none_stop=True), daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
