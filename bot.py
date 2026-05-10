import telebot
from flask import Flask
from mcrcon import MCRcon
import threading

TOKEN = '8737751023:AAGjcTZIADQ86f3AyURHq0KiP5X4UocX4a0'
ADMIN_ID = 8648741496
RCON_HOST = 'localhost'
RCON_PORT = 25575
RCON_PASS = 'GrifMC_Admin_2026'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def rcon_cmd(command):
    try:
        with MCRcon(RCON_HOST, RCON_PASS, port=RCON_PORT, timeout=3) as client:
            response = client.command(command)
            return response if response else "✅ Выполнено"
    except Exception as e:
        return f"❌ Ошибка: {e}"

@app.route('/')
def home():
    return "RCON Bot работает!"

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "🛠️ **GrifMC RCON Бот**\n\n"
        "`!rcon tps` — TPS\n"
        "`!rcon list` — онлайн\n"
        "`!rcon say текст` — чат\n"
        "`!rcon команда` — любая"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_rcon(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Только админ!")
        return
    
    text = message.text.strip()
    if not text.startswith('!rcon'):
        bot.send_message(message.chat.id, "Используй `!rcon команда`", parse_mode="Markdown")
        return
    
    command = text[6:].strip()
    if not command:
        bot.send_message(message.chat.id, "❌ `!rcon команда`", parse_mode="Markdown")
        return
    
    response = rcon_cmd(command)
    if len(response) > 4000:
        response = response[:3900] + "..."
    
    bot.send_message(message.chat.id, f"```\n{response}\n```", parse_mode="Markdown")

def run_bot():
    print("RCON Bot started!")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
