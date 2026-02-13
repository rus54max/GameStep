import random
import os
import time

# === ИГРОВЫЕ ДАННЫЕ ===

# Карта подземелья (словарь комнат с выходами и содержимым)
dungeon = {
        'вход': {
        'описание': 'Вы стоите у входа в темное подземелье. Факелы освещают каменный коридор, уходящий вглубь.',
        'выходы': {'север': 'коридор'},
        'враги': [],
        'предметы': ['факел']
    },
        'коридор': {
        'описание': 'Длинный коридор с влажными стенами.',
        'выходы': {'север': 'развилка', 'юг': 'вход'},
        'враги': ['крыса'],
        'предметы': []
    },
        'развилка': {
        'описание': 'Коридор разветвляется на восток и запад.',
        'выходы': {'восток': 'оружейная', 'запад': 'логово', 'юг': 'коридор'},
        'враги': ['скелет'],
        'предметы': []
    },
        'оружейная': {
        'описание': 'Старая оружейная. Большинство оружия проржавело, но кое-что можно использовать.',
        'выходы': {'запад': 'развилка', 'север': 'сокровищница'},
        'враги': [],
        'предметы': ['меч', 'щит']
    },
        'логово': {
        'описание': 'Мрачное логово с костями на полу.',
        'выходы': {'восток': 'развилка'},
        'враги': ['огр'],
        'предметы': ['зелье']
    },
        'сокровищница': {
        'описание': 'Комната, полная золота и драгоценностей!',
        'выходы': {'юг': 'оружейная'},
        'враги': ['дракон'],
        'предметы': ['сокровище']
    }
}

# Характеристики врагов
enemies = {
    'крыса': {'здоровье': 10, 'атака': 2, 'защита': 0, 'опыт': 5},
    'скелет': {'здоровье': 20, 'атака': 4, 'защита': 1, 'опыт': 10},
    'огр': {'здоровье': 30, 'атака': 6, 'защита': 2, 'опыт': 20},
    'дракон': {'здоровье': 50, 'атака': 8, 'защита': 4, 'опыт': 50}
    }

# Предметы
items = {
    'факел': {'тип': 'инструмент', 'описание': 'Освещает темные комнаты'},
    'меч': {'тип': 'оружие', 'описание': 'Увеличивает атаку на 5', 'бонус': 5},
    'щит': {'тип': 'защита', 'описание': 'Увеличивает защиту на 3', 'бонус': 3},
    'зелье': {'тип': 'зелье', 'описание': 'Восстанавливает 20 здоровья', 'бонус': 20},
    'сокровище': {'тип': 'цель', 'описание': 'Легендарное сокровище подземелья!'}
    }

# === ИГРОВЫЕ ФУНКЦИИ ===

def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def init_player():
    """Инициализирует игрока"""
    return {
        'здоровье': 100,
        'макс_здоровье': 100,
        'атака': 5,
        'защита': 2,
        'опыт': 0,
        'уровень': 1,
        'инвентарь': [],
        'текущая_комната': 'вход'
        }

def display_stats(player):
    """Отображает статистику игрока"""
    print("\n=== СТАТИСТИКА ИГРОКА ===")
    print(f"Здоровье: {player['здоровье']}/{player['макс_здоровье']}")
    print(f"Атака: {player['атака']} | Защита: {player['защита']}")
    print(f"Уровень: {player['уровень']} | Опыт: {player['опыт']}")
    print(f"Инвентарь: {', '.join(player['инвентарь']) if player['инвентарь'] else 'пусто'}")
    print("=========================")

def display_room(player):
    """Отображает информацию о текущей комнате"""
    room = dungeon[player['текущая_комната']]

    print(f"\n{room['описание']}")

    # Выходы
    exits = list(room['выходы'].keys())
    print(f"Выходы: {', '.join(exits)}")

    # Враги
    if room['враги']:
        print(f"Осторожно! Здесь есть: {', '.join(room['враги'])}")

    # Предметы
    if room['предметы']:
        print(f"Вы видите: {', '.join(room['предметы'])}")

def move_player(player, direction):
    """Перемещает игрока в указанном направлении"""
    current_room = dungeon[player['текущая_комната']]

    if direction in current_room['выходы']:
        player['текущая_комната'] = current_room['выходы'][direction]
        return True, f"Вы идете на {direction}."
    else:
        return False, "Вы не можете идти в этом направлении."

def take_item(player, item_name):
    """Подбирает предмет и добавляет в инвентарь"""
    room = dungeon[player['текущая_комната']]

    if item_name in room['предметы']:
        room['предметы'].remove(item_name)
        player['инвентарь'].append(item_name)

        # Применяем эффект предмета
        item = items[item_name]
        if item['тип'] == 'оружие':
            player['атака'] += item['бонус']
        elif item['тип'] == 'защита':
            player['защита'] += item['бонус']

        return True, f"Вы подобрали {item_name}."
    else:
        return False, f"Здесь нет {item_name}."

def use_item(player, item_name):
    """Использует предмет из инвентаря"""
    if item_name in player['инвентарь']:
        item = items[item_name]

        if item['тип'] == 'зелье':
            player['здоровье'] = min(player['здоровье'] + item['бонус'], player['макс_здоровье'])
            player['инвентарь'].remove(item_name)
            return True, f"Вы использовали {item_name} и восстановили {item['бонус']} здоровья."
        else:
            return False, f"Вы не можете использовать {item_name}."
    else:
        return False, f"У вас нет {item_name}."

def combat(player, enemy_name):
    """Проводит бой с врагом"""
    enemy = enemies[enemy_name].copy() # Копируем, чтобы не изменить оригинал

    print(f"\nНачинается бой с {enemy_name}!")
    time.sleep(1)

    while player['здоровье'] > 0 and enemy['здоровье'] > 0:
        # Ход игрока
        player_damage = max(1, player['атака'] - enemy['защита'])
        enemy['здоровье'] -= player_damage
        print(f"Вы атакуете {enemy_name} и наносите {player_damage} урона!")

        if enemy['здоровье'] <= 0:
            print(f"Вы победили {enemy_name}!")
            player['опыт'] += enemy['опыт']
            check_level_up(player)

            # Удаляем врага из комнаты
            dungeon[player['текущая_комната']]['враги'].remove(enemy_name)
            return True

        time.sleep(0.5)

        # Ход врага
        enemy_damage = max(1, enemy['атака'] - player['защита'])
        player['здоровье'] -= enemy_damage
        print(f"{enemy_name} атакует вас и наносит {enemy_damage} урона!")

        if player['здоровье'] <= 0:
            print("Вы погибли...")
            return False

        # Статус боя
        print(f"Ваше здоровье: {player['здоровье']} | Здоровье {enemy_name}: {enemy['здоровье']}")
        time.sleep(1)

def check_level_up(player):
    """Проверяет, достиг ли игрок нового уровня"""
    exp_needed = player['уровень'] * 20

    if player['опыт'] >= exp_needed:
        player['уровень'] += 1
        player['атака'] += 2
        player['защита'] += 1
        player['макс_здоровье'] += 10
        player['здоровье'] = player['макс_здоровье']
        print(f"\nПоздравляем! Вы достигли уровня {player['уровень']}!")
        print("Ваши характеристики улучшились!")

def check_room_enemies(player):
    """Проверяет, есть ли враги в комнате, и инициирует бой"""
    room = dungeon[player['текущая_комната']]

    if room['враги']:
        enemy = room['враги'][0]
        return combat(player, enemy)

    return True # Нет врагов, можно продолжать

def check_victory(player):
    """Проверяет условия победы"""
    return 'сокровище' in player['инвентарь'] and player['текущая_комната'] == 'вход'

def process_command(player, command):
    """Обрабатывает команду игрока"""
    parts = command.split(maxsplit=1)
    action = parts[0].lower() if parts else ""
    target = parts[1].lower() if len(parts) > 1 else ""

    if action == "идти" and target:
        return move_player(player, target)
    elif action == "взять" and target:
        return take_item(player, target)
    elif action == "использовать" and target:
        return use_item(player, target)
    elif action == "осмотреться":
        return True, "Вы внимательно осматриваетесь."
    elif action == "инвентарь":
        items_desc = [f"{item}: {items[item]['описание']}" for item in player['инвентарь']]
        return True, f"Ваш инвентарь: {', '.join(items_desc) if items_desc else 'пусто'}"
    elif action == "помощь":
        help_text = """
        Доступные команды:
        - идти [направление] (север, юг, восток, запад)
        - взять [предмет]
        - использовать [предмет]
        - осмотреться
        - инвентарь
        - помощь
        - выход
        """
        return True, help_text
    elif action == "выход":
        return "exit", "Выход из игры."
    else:
        return False, "Я не понимаю эту команду. Введите 'помощь' для списка команд."

# === ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ===

def play_game():
    """Основная функция игры"""
    clear_screen()
    print("=== ПОДЗЕМЕЛЬЕ ДРАКОНА ===")
    print("Вы отважный искатель приключений, который должен найти")
    print("сокровище в подземелье дракона и вынести его наружу.")
    print("Введите 'помощь' для списка команд.")

    player = init_player()
    game_running = True

    while game_running and player['здоровье'] > 0:
        # Отображаем информацию о комнате и персонаже
        display_room(player)
        display_stats(player)

        # Проверяем, есть ли враги в комнате
        if dungeon[player['текущая_комната']]['враги']:
            survived = check_room_enemies(player)
            if not survived:
                break

        # Проверяем условия победы
        if check_victory(player):
            clear_screen()
            print("=== ПОЗДРАВЛЯЕМ! ===")
            print("Вы нашли сокровище и успешно выбрались из подземелья!")
            print(f"Вы завершили игру на уровне {player['уровень']} с {player['опыт']} очками опыта.")
            break

        # Получаем и обрабатываем команду игрока
        command = input("\nЧто будете делать? > ")
        result, message = process_command(player, command)

        if result == "exit":
            game_running = False

        print(message)
        time.sleep(1)
        clear_screen()

        if player['здоровье'] <= 0:
            print("=== ИГРА ОКОНЧЕНА ===")
            print("Вы погибли в подземелье. Ваше приключение завершено.")

    print("\nСпасибо за игру!")

if __name__ == "__main__":
    play_game()