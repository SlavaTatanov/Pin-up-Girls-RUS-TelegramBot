from datetime import date

class Counter:
    def __init__(self):
        """Создает счетчик"""
        self.counter = {}

    def add_id(self, user):
        """
        Добавляет ид пользователя в сет для текущей даты,
        если есть старые даты удаляет их
        """
        cur_date = date.today()
        if cur_date not in self.counter:
            self.counter[cur_date] = {user}
        else:
            self.counter[cur_date].add(user)
        if len(self.counter) > 1:
            self.clear(cur_date)

    def clear(self, cur_date):
        """
        Удаляет старые даты
        """
        key_not_actual = []
        for key in self.counter:
            if key != cur_date:
                key_not_actual.append(key)
        for key in key_not_actual:
            del self.counter[key]

    def user_count(self):
        """
        Возвращает количество уникальных пользователей
        """
        cur_date = date.today()
        if cur_date in self.counter:
            return f"{len(self.counter[cur_date])} пользователей {cur_date}"
        else:
            return f"0 пользователей {cur_date}"
