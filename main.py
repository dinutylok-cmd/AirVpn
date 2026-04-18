import flet as ft
import telebot
import threading
import time

TOKEN = "8640024441:AAGLqms9l4_luuro1XSuxBDISJAfu1xD3io"

# Запуск бота с полной изоляцией ошибок
def bot_worker():
    try:
        bot = telebot.TeleBot(TOKEN)
        @bot.message_handler(func=lambda m: True)
        def echo_all(m):
            bot.reply_to(m, "System Online")
        bot.polling(none_stop=True)
    except:
        time.sleep(10)
        bot_worker()

threading.Thread(target=bot_worker, daemon=True).start()

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#101217"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Контент, который ДОЛЖЕН появиться
    page.add(
        ft.Icon(ft.icons.SHIELD_LOCK, size=100, color="#007AFF"),
        ft.Text("AirVpn", size=32, weight="bold"),
        ft.ElevatedButton("CONNECT", width=200, bgcolor="#007AFF", color="white")
    )
    page.update()

ft.app(target=main)
