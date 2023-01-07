import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def unit_exists(self, unit_name):
        """Проверяем, есть ли установка в базе"""
        result = self.cursor.execute("SELECT `unit_id` FROM `units` WHERE `unit_name` = ?", (unit_name,))
        return bool(len(result.fetchall()))

    def get_unit_id(self, unit_name):
        """Достаем unit_id установки в базе по его unit_name"""
        result = self.cursor.execute("SELECT `unit_id` FROM `units` WHERE `unit_name` = ?", (unit_name,))
        return result.fetchone()[0]

    def get_all_unit_list(self):
        """Достаем unit_id установки в базе по его unit_name"""
        result = self.cursor.execute("SELECT unit_name FROM units")
        return result.fetchall()

    def add_unit(self, unit_name):
        """Добавляем установку в базу"""
        self.cursor.execute("INSERT INTO `units` (`unit_name`) VALUES (?)", (unit_name,))
        return self.conn.commit()

    def add_record(self, unit_name, spare_parts_name, count, date):
        """Создаем запись о cписании"""
        self.cursor.execute("INSERT INTO `records` (`units_id`, `spare_parts_name`, `count`, `date`) VALUES (?, ?, ?, ?)",
            (self.get_unit_id(unit_name),
            spare_parts_name,
            count,
            date))
        return self.conn.commit()

    def get_records(self, start_date, end_date):
        """Получаем историю списания"""
        result = self.cursor.execute("SELECT record_id, unit_name, spare_parts_name, count, date  "
                                     "FROM units INNER JOIN records"
                                     " ON units.unit_id = records.units_id"
                                     " WHERE date  BETWEEN date(?) AND date(?) ORDER BY date",
                                     (start_date,
                                     end_date))

        columns = [el[0] for el in self.cursor.description]

        return columns,  result.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
