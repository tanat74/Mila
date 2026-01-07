import requests
import os
import sys
from urllib.parse import quote

# ============================================================================
# УПРАВЛЯЮЩИЕ ПАРАМЕТРЫ - ИЗМЕНИТЕ ЗДЕСЬ
# ============================================================================

# Фраза для записи
TEXT = "Мила"

# Русские голоса RHVoice
VOICES = [
    "aleksandr", "aleksandr-hq", "anna", "arina", "artemiy", 
    "elena", "evgeniy-rus", "irina", "mikhail", "pavel", 
    "tatiana", "timofey", "umka", "victoria", "vitaliy", 
    "vitaliy-ng", "vsevolod", "yuriy"
]

# Параметры rate, pitch, volume (от 20 до 90 с шагом 5)
RATE_PITCH_VOLUME_RANGE = range(90, 110, 10)  # 20, 25, 30, ..., 90

# Каталог сохранения
OUTPUT_DIR = r"D:\Linux\microWakeWord-Trainer\generated_samples"

# Адрес RHVoice REST сервера
RHVOICE_SERVER = "http://localhost:8080"

# Формат файла
FORMAT = "wav"

# ============================================================================
# ПРОВЕРКА ДОСТУПНОСТИ СЕРВЕРА
# ============================================================================

def check_server_availability():
    """
    Проверяет доступность RHVoice REST сервера.
    Если сервер недоступен, прерывает выполнение.
    """
    try:
        print(f"🔍 Проверка доступности сервера {RHVOICE_SERVER}...")
        response = requests.get(f"{RHVOICE_SERVER}/info", timeout=5)
        response.raise_for_status()
        print("✅ Сервер доступен!\n")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Ошибка подключения: не удается подключиться к {RHVOICE_SERVER}")
        print("   Убедитесь, что контейнер rhvoice-rest запущен")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"❌ Ошибка: сервер {RHVOICE_SERVER} не отвечает (timeout)")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при проверке сервера: {e}")
        sys.exit(1)


# ============================================================================
# ОСНОВНОЙ МЕТОД - ГЕНЕРИРУЕТ СЭМПЛЫ ДЛЯ ВСЕХ ГОЛОСОВ И ПАРАМЕТРОВ
# ============================================================================

def generate_all_samples(text=TEXT, voices=VOICES, output_dir=OUTPUT_DIR):
    """
    Генерирует сэмплы для всех голосов и параметров.
    
    Args:
        text: Фраза для записи
        voices: Список голосов
        output_dir: Каталог сохранения
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, voice in enumerate(voices, 1):
        print(f"🎤 Голос {idx} / {len(voices)}: {voice}")
        for rate in RATE_PITCH_VOLUME_RANGE:
            for pitch in RATE_PITCH_VOLUME_RANGE:
                for volume in RATE_PITCH_VOLUME_RANGE:
                    filename = f"{voice}_rate{rate}_pitch{pitch}_volume{volume}.{FORMAT}"
                    filepath = os.path.join(output_dir, filename)
                    
                    try:
                        save_sample(text, voice, rate, pitch, volume, filepath)
                    except Exception as e:
                        print(f"  ❌ Ошибка: {e}")
                        continue
    
    print(f"\n✅ Готово! Сэмплы сохранены в: {output_dir}")


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЙ МЕТОД - ВЫЗЫВАЕТ СЕРВЕР И СОХРАНЯЕТ ФАЙЛ
# ============================================================================

def save_sample(text, voice, rate, pitch, volume, filepath):
    """
    Вызывает RHVoice REST API и сохраняет файл.
    
    Args:
        text: Текст для синтеза
        voice: Голос
        rate: Темп речи (0-100)
        pitch: Высота голоса (0-100)
        volume: Громкость (0-100)
        filepath: Путь для сохранения файла
    """
    encoded_text = quote(text)
    
    url = (f"{RHVOICE_SERVER}/say?"
           f"text={encoded_text}"
           f"&voice={voice}"
           f"&format={FORMAT}"
           f"&rate={rate}"
           f"&pitch={pitch}"
           f"&volume={volume}")
    
    response = requests.get(url)
    response.raise_for_status()
    
    with open(filepath, 'wb') as f:
        f.write(response.content)


# ============================================================================
# ТЕСТОВЫЙ МЕТОД - ГЕНЕРИРУЕТ СЭМПЛЫ С ФИКСИРОВАННЫМИ ПАРАМЕТРАМИ (50)
# ============================================================================

def generate_test_samples(text=TEXT, voices=VOICES, output_dir=OUTPUT_DIR):
    """
    Генерирует тестовые сэмплы с фиксированными параметрами (rate=50, pitch=50, volume=50).
    Меняются только голоса.
    
    Args:
        text: Фраза для записи
        voices: Список голосов
        output_dir: Каталог сохранения
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, voice in enumerate(voices, 1):
        print(f"🎤 Голос {idx} / {len(voices)}: {voice}")
        filename = f"{voice}_rate50_pitch50_volume50.{FORMAT}"
        filepath = os.path.join(output_dir, filename)
        
        try:
            save_sample(text, voice, 50, 50, 50, filepath)
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            continue
    
    print(f"\n✅ Тестирование завершено! Сэмплы сохранены в: {output_dir}")


# ============================================================================
# ПРИМЕРЫ ЗАПУСКА
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python generate_samples.py test  - быстрый тест (18 файлов)")
        print("  python generate_samples.py full  - полная генерация (много файлов)")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    # Проверяем доступность сервера перед началом
    check_server_availability()
    
    if mode == "test":
        print("🔄 Запуск тестового режима...")
        generate_test_samples()
    elif mode == "full":
        print("🔄 Запуск полного режима...")
        generate_all_samples()
    else:
        print(f"❌ Неизвестный режим: {mode}")
        print("Используйте 'test' или 'full'")
        sys.exit(1)
