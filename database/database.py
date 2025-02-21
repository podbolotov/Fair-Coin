import sqlite3

from models.coins import CoinSidesChances
from core.vars import ServiceVariables

class Database:
    def __init__(self):
        self.storage='storage/database.db'
        connection = sqlite3.connect(self.storage)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chances (
            id INTEGER PRIMARY KEY,
            head_chance INTEGER NOT NULL,
            tail_chance INTEGER NOT NULL
        )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chances (
            id INTEGER PRIMARY KEY,
            head_chance INTEGER NOT NULL,
            tail_chance INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            timestamp DATE DEFAULT (datetime('now','localtime')),
            result TEXT NOT NULL,
            chances TEXT NOT NULL
            )
        ''')

        cursor.execute('INSERT OR IGNORE INTO chances (id, head_chance, tail_chance) VALUES (?, ?, ?)',
                       (1, 50, 50))

        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

    def get_chances(self) -> CoinSidesChances:
        connection = sqlite3.connect(self.storage)
        cursor = connection.cursor()
        cursor.execute('SELECT head_chance, tail_chance FROM chances WHERE id = 1;')
        db_result = cursor.fetchone()
        connection.close()
        return CoinSidesChances(HEAD=db_result[0], TAIL=db_result[1])


    def write_chances(self, head_chance: int, tail_chance: int):
        connection = sqlite3.connect(self.storage)
        cursor = connection.cursor()
        cursor.execute('UPDATE chances SET head_chance = ?, tail_chance = ? WHERE id = 1',
                       (head_chance, tail_chance))
        connection.commit()
        connection.close()

    def get_history(self):
        connection = sqlite3.connect(self.storage)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM history ORDER BY timestamp DESC;')
        db_result = cursor.fetchall()
        connection.close()
        return db_result


    def write_to_history(self, result: str, chances: str):
        connection = sqlite3.connect(self.storage)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO history (result, chances) VALUES (?, ?)',
                       (result, chances))
        connection.commit()
        connection.close()

    def shrink_history(self, shrink_to: int = ServiceVariables.SHRINK_HISTORY_TO):
        connection = sqlite3.connect(self.storage)
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY timestamp DESC LIMIT ?)',
            (str(shrink_to),)
        )
        connection.commit()
        connection.close()