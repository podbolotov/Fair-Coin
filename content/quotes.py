import random

before_flip_quotes = [
    'Судьба - вредина 👹',
    'Мы не рады случаю, но полагаемся на него 🤨',
    'Пусть мне повезёт 🤞',
    'Пусть оппоненту не повезёт 🤞',
    'Икота, перейди на Федота 🥴',
    'Сколько уже можно то 😤',
    '😣 Сил моих больше нет',
    'А можно не надо? 🙃',
    '🤔 Давай уже, бросай',
    'Ожидание не увеличивает шансы 🤓',
    'Тебе повезёт. Но это не точно 🙂',
    'Монеток бояться - на эту страничку не ходить ✊',
    '🧐 Тише едешь - позже приедешь'
]

after_flip_quotes = [
    '👀 Результат пересмотру не подлежит',
    '😑 Смирение - это правильно',
    '🤬 Бесячий результат - тоже результат',
    'Слёзы делу не подмога 😿',
    'Ой ёй 👉👈',
    'Монетка лжёт 🤥',
    'Нечестная монетка 😒',
    'Ну вот, посмотри до чего ты меня доводишь 🤌',
    'Всё подстроено! 👺'
]

def get_random_before_flip_quote():
    return random.choice(before_flip_quotes)

def get_random_after_flip_quote():
    return random.choice(after_flip_quotes)