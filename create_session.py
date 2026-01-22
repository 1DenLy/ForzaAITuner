import json
import os
import uuid
from datetime import datetime

SESSION_DIR = 'data'
LAST_SESSION_FILE = 'last_session_config.json'


def get_input(prompt, default_value=None):
    """
    Умный ввод: показывает старое значение.
    """
    if default_value is not None:
        user_input = input(f"{prompt} [{default_value}]: ")
        if user_input.strip() == "":
            return default_value
    else:
        user_input = input(f"{prompt}: ")

    # Пытаемся превратить в число, если это возможно
    try:
        return float(user_input)
    except ValueError:
        return user_input


def create_session():
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    # 1. Загружаем предыдущие настройки
    defaults = {}
    if os.path.exists(LAST_SESSION_FILE):
        try:
            with open(LAST_SESSION_FILE, 'r') as f:
                defaults = json.load(f)
            print(">>> Загружены данные предыдущего заезда.")
        except:
            pass

    print("\n=== НАСТРОЙКИ ТЮНИНГА ===\n")

    # --- ВЫБОР ПРИВОДА ---
    print("--- [1] Привод (Drivetrain) ---")
    # Берем старое значение или ставим RWD по умолчанию
    def_drive = defaults.get("drivetrain_type", "RWD")
    drivetrain = str(get_input("Тип привода (RWD/AWD/FWD)", def_drive)).upper()

    # --- ДИФФЕРЕНЦИАЛ (Зависит от привода) ---
    print(f"\n--- [2] Дифференциал ({drivetrain}) ---")
    diff_settings = {}

    # Загружаем старые настройки диффа (если были)
    old_diff = defaults.get("diff", {})

    if drivetrain == "AWD":
        # Полный привод: Перед, Зад, Центр
        diff_settings["front_accel"] = get_input("Перед. Ускорение %", old_diff.get("front_accel"))
        diff_settings["front_decel"] = get_input("Перед. Торможение %", old_diff.get("front_decel"))
        diff_settings["rear_accel"] = get_input("Зад. Ускорение %", old_diff.get("rear_accel"))
        diff_settings["rear_decel"] = get_input("Зад. Торможение %", old_diff.get("rear_decel"))
        diff_settings["center_balance"] = get_input("Центр. баланс (на зад) %", old_diff.get("center_balance"))

    elif drivetrain == "RWD":
        # Задний привод: Только зад
        diff_settings["rear_accel"] = get_input("Зад. Ускорение %", old_diff.get("rear_accel"))
        diff_settings["rear_decel"] = get_input("Зад. Торможение %", old_diff.get("rear_decel"))

    elif drivetrain == "FWD":
        # Передний привод: Только перед
        diff_settings["front_accel"] = get_input("Перед. Ускорение %", old_diff.get("front_accel"))
        diff_settings["front_decel"] = get_input("Перед. Торможение %", old_diff.get("front_decel"))

    # --- ПОДВЕСКА И ШИНЫ ---
    print("\n--- [3] Шины ---")
    tires = {
        "psi_front": get_input("Давление ПЕРЕД (Bar/PSI)", defaults.get("tires", {}).get("psi_front")),
        "psi_rear": get_input("Давление ЗАД (Bar/PSI)", defaults.get("tires", {}).get("psi_rear"))
    }

    print("\n--- [4] Развал/Схождение ---")
    alignment = {
        "camber_front": get_input("Развал ПЕРЕД", defaults.get("alignment", {}).get("camber_front")),
        "camber_rear": get_input("Развал ЗАД", defaults.get("alignment", {}).get("camber_rear")),
        "toe_front": get_input("Схождение ПЕРЕД", defaults.get("alignment", {}).get("toe_front")),
        "toe_rear": get_input("Схождение ЗАД", defaults.get("alignment", {}).get("toe_rear")),
        "caster": get_input("Кастер", defaults.get("alignment", {}).get("caster"))
    }

    print("\n--- [5] Пружины ---")
    springs = {
        "stiffness_front": get_input("Пружины ПЕРЕД (кг/мм)", defaults.get("springs", {}).get("stiffness_front")),
        "stiffness_rear": get_input("Пружины ЗАД (кг/мм)", defaults.get("springs", {}).get("stiffness_rear")),
        "ride_height_front": get_input("Клиренс ПЕРЕД", defaults.get("springs", {}).get("ride_height_front")),
        "ride_height_rear": get_input("Клиренс ЗАД", defaults.get("springs", {}).get("ride_height_rear"))
    }

    print("\n--- [6] Стабилизаторы (ARB) ---")
    arb = {
        "front": get_input("Стаб ПЕРЕД", defaults.get("arb", {}).get("front")),
        "rear": get_input("Стаб ЗАД", defaults.get("arb", {}).get("rear"))
    }

    print("\n--- [7] Амортизация ---")
    damping = {
        "rebound_front": get_input("Отбой ПЕРЕД", defaults.get("damping", {}).get("rebound_front")),
        "rebound_rear": get_input("Отбой ЗАД", defaults.get("damping", {}).get("rebound_rear")),
        "bump_front": get_input("Сжатие ПЕРЕД", defaults.get("damping", {}).get("bump_front")),
        "bump_rear": get_input("Сжатие ЗАД", defaults.get("damping", {}).get("bump_rear"))
    }

    # Сборка финального объекта
    tuning_data = {
        "drivetrain_type": drivetrain,
        "diff": diff_settings,
        "tires": tires,
        "alignment": alignment,
        "springs": springs,
        "arb": arb,
        "damping": damping
    }

    # Генерация ID (время + короткий код)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_id = f"{timestamp}"

    final_data = {
        "session_id": session_id,
        "tuning": tuning_data
    }

    # Сохраняем "последние настройки" для следующего раза
    with open(LAST_SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(tuning_data, f, indent=4, ensure_ascii=False)

    # Сохраняем саму сессию
    filename = os.path.join(SESSION_DIR, f"tuning_{session_id}.json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print("\n" + "=" * 40)
    print(f"✅ Файл настроек создан: tuning_{session_id}.json")
    print(f"🔑 ID СЕССИИ (копируй это): {session_id}")
    print("=" * 40)


if __name__ == "__main__":
    create_session()