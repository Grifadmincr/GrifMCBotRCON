import telebot
from threading import Thread
from flask import Flask
from rcon import Client

TOKEN = '8737751023:AAGjcTZIADQ86f3AyURHq0KiP5X4UocX4a0'
ADMIN_ID = 8648741496
RCON_HOST = 'localhost'
RCON_PORT = 25575
RCON_PASS = 'GrifMC_Admin_2026'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def rcon_cmd(command):
    try:
        with Client(RCON_HOST, RCON_PORT, passwd=RCON_PASS, timeout=3) as client:
            response = client.run(command)
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
        "Команды:\n"
        "`!rcon tps` — TPS сервера\n"
        "`!rcon list` — игроки онлайн\n"
        "`!rcon bcast текст` — объявление\n"
        "`!rcon say текст` — в чат\n"
        "`!rcon give ник предмет кол-во`\n"
        "`!rcon ban ник причина`\n"
        "`!rcon kick ник причина`\n"
        "`!rcon команда` — любая команда"
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
        bot.send_message(message.chat.id, "❌ `!rcon команда`\nНапример: `!rcon tps`", parse_mode="Markdown")
        return
    
    response = rcon_cmd(command)
    if len(response) > 4000:
        response = response[:3900] + "...(обрезано)"
    
    bot.send_message(message.chat.id, f"```\n{response}\n```", parse_mode="Markdown")

def run_bot():
    print("RCON Bot started!")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
