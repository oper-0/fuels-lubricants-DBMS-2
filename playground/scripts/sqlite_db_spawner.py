import calendar
import csv
import random
import sqlite3
import datetime
import time

from typing import NamedTuple


#       STRUCTS:
class table_headers(NamedTuple):
    table_name: str
    headers: list[str]


class sqlite_database_spawner:
    def __init__(self):
        self.database_path = r"C:\Users\4NR_Operator_34\Favorites\chernika-34\dev\SW\normGSM\0\fuels-lubricants-DBMS\source\databases\test_db_1.db"

        self.con = None
        self.cur = None

    def populate(self):
        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()

        self.populate_vehicle()
        self.populate_measureUnits()
        self.populate_norm_61()
        self.populate_unit()

        self.con.close()

    def clear_all(self):
        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()

        self.cur.execute('DELETE FROM MeasureUnits;', )
        self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE NAME='MeasureUnits';", )

        self.cur.execute('DELETE FROM Vehicle;', )
        self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE NAME='Vehicle';", )

        self.cur.execute('DELETE FROM Norm_61;', )
        self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE NAME='Norm_61';", )

        self.cur.execute('DELETE FROM Unit;', )
        self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE NAME='Unit';", )

        self.con.commit()
        self.con.close()

        print('[INFO]\tall tables are cleared.')

    def populate_unit(self):
        result: list[dict] = []
        path = r'C:\Users\4NR_Operator_34\Favorites\chernika-34\dev\SW\normGSM\fuels-lubricants-DBMS\source\Infrastructure\Repositories\InMemory_normDB\pivot_records.csv'

        query = 'SELECT * FROM Vehicle'
        self.cur.execute(query)
        vehicles_unique_names = self.cur.fetchall()
        vehicles_unique_names = [u[1] for u in vehicles_unique_names]

        query = 'SELECT * FROM Norm_61'
        self.cur.execute(query)
        unit_fuel_consumption = self.cur.fetchall()
        unit_fuel_consumption = [u[0] for u in unit_fuel_consumption]

        with open(path, encoding='windows-1251') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            counter = 0
            for row in csv_reader:
                counter += 1
                data = {
                    # 'unitSerialNumber': row[0],
                    'military_agency': row[1],
                    'unit_name': row[2],
                    'unit_code': row[3],
                    'unit_base_vehicle': random.choice(vehicles_unique_names),
                    'unit_ICE': row[5],
                    'equipment_engine': row[6],
                    'unit_fuel_consumption': random.choice(unit_fuel_consumption),
                    # 'vehicle_fuel_consumption': None,
                    # 'equipment_fuel_consumption': None,
                }

                query = 'INSERT INTO Unit({}) VALUES({})'.format(', '.join(list(data.keys())),
                                                                 ', '.join(['?' for i in data.keys()])
                                                                 )
                TO_RECORD = tuple(list(data.values()))

                self.cur.execute(query, TO_RECORD)

        print("[last id:{}] populated Unit table (recorded {} rows)".format(self.cur.lastrowid, counter))
        self.con.commit()

        # print(f'Processed {line_count} lines.')
        # print('data:{}'.format(result))
        return result

    def clear_norm_61(self):
        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()

        self.cur.execute('DELETE FROM Norm_61;', )
        self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE NAME='Norm_61';", )

        self.con.commit()
        self.con.close()

        print('[INFO]\tNorm_61 is cleared.')

    def populate_norm_61(self):
        records_number = 100

        query = 'SELECT * FROM MeasureUnits'
        self.cur.execute(query)
        measure_units = self.cur.fetchall()
        measure_units = [u[0] for u in measure_units]

        data = {
            'benzin_consumption_per_distance': lambda: random.randint(400, 600) * 0.1,
            'diesel_consumption_per_distance': lambda: random.randint(400, 600) * 0.1,
            'per_distance_measure_unit': '',  # 'л/км',???? ✅
            'benzin_consumption_per_hour_in_move': lambda: random.randint(400, 600) * 0.1,
            'diesel_consumption_per_hour_in_move': lambda: random.randint(400, 600) * 0.1,
            'benzin_consumption_per_hour_on_stop': lambda: random.randint(400, 600) * 0.1,
            'diesel_consumption_per_hour_on_stop': lambda: random.randint(400, 600) * 0.1,
            'per_hour_measure_unit': '',  # random.choice(['л', 'кг']), ???? ✅
            'engine_oils_consuption': lambda: random.randint(5, 30) * 0.1,
            'engine_oil_measure_unit': '',  # random.choice(['л/ч', 'кг/ч']), ???? ✅
            'ethyl_consumption': lambda: random.randint(1, 10) * 0.1,
            'ethyl_measure_unit': '',  # '% от расхода топлива', ???? ✅
            'approval_date': lambda: random_date("01/04/2021", "01/04/2023", random.random()),
            'validity_duration': lambda: random.choice([5, 12, 36, 60]),
            'validity_duration_unit': '',  # ufc_validity_duration_unit, ????? ✅
            'expiring_date': None
        }

        for i in range(records_number):
            # query = ''' INSERT INTO Norm_61({})
            #             VALUES({})
            #  '''.format(', '.join(list(data.keys())), ', '.join(['?' for i in data.keys()]))
            # # '''.format(', '.join(['?' for i in data.keys()]))
            t_approval_data_str, t_approval_data = data['approval_date']()
            t_validity_duration = data['validity_duration']()
            t_expiring_date = add_months(datetime.datetime.strptime(t_approval_data_str, "%d/%m/%Y").date(),
                                         t_validity_duration)

            query = 'INSERT INTO Norm_61({}) VALUES({})'.format(', '.join(list(data.keys())),
                                                                ', '.join(['?' for i in data.keys()])
                                                                )

            TO_RECORD = (
                round(data['benzin_consumption_per_distance'](), 3),
                round(data['diesel_consumption_per_distance'](), 3),
                random.choice(measure_units),
                round(data['benzin_consumption_per_hour_in_move'](), 3),
                round(data['diesel_consumption_per_hour_in_move'](), 3),
                round(data['benzin_consumption_per_hour_on_stop'](), 3),
                round(data['diesel_consumption_per_hour_on_stop'](), 3),
                random.choice(measure_units),
                round(data['engine_oils_consuption'](), 3),
                random.choice(measure_units),
                round(data['ethyl_consumption'](), 3),
                random.choice(measure_units),
                t_approval_data,
                t_validity_duration,
                random.choice(measure_units),
                t_expiring_date
            )

            self.cur.execute(query, TO_RECORD)

        # for i in range(records_number):
        #     query = ''' INSERT INTO Norm_61(per_distance_measure_unit,
        #                                     per_hour_measure_unit,
        #                                     engine_oil_measure_unit,
        #                                     ethyl_measure_unit,
        #                                     validity_duration_unit)
        #                 VALUES(?, ?, ?, ?, ?)
        #     '''
        #
        #     print(query)
        #
        #     self.cur.execute(query, (
        #         random.choice(measure_units),
        #         random.choice(measure_units),
        #         random.choice(measure_units),
        #         random.choice(measure_units),
        #         random.choice(measure_units),
        #     ))

        print("[last id:{}] populated Norm_61 table (recorded {} rows)".format(self.cur.lastrowid, records_number))
        self.con.commit()

    def populate_measureUnits(self):

        data_list = [
            ("л.", "литр"),
            ("кг.", "килограмм"),
            ("л/ч", "литры в час"),
            ("кг/ч", "килограмм в час"),
            ("%", "% от расхода горючего"),
            ("г.", "грамм")
        ]

        query = ''' INSERT INTO MeasureUnits(unit, full_name)
                    VALUES(?, ?)'''
        for data in data_list:
            self.cur.execute(query, data)
        print("[last id:{}] populated MeasureUnits table (recorded {} rows)".format(self.cur.lastrowid, len(data_list)))
        self.con.commit()

    def populate_vehicle(self):

        data_list = [
            (
                'КАМАЗ-4308-81(N5) на КПГ', 'Автомобиль грузовой',
                bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-4308-69 (G5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-43253-69 (G5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-53605-37 на КПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-53605-48 (A5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-43255-69 (G5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-43502-66 (D5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-5308-48 (A5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-43118-37 на CПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-43118-37 на КПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-5350-37 на КПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-43118-50', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-5350-66 (D5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-63501-52', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65111-50', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65115-37 на СПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65115-37 на КПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65115-48 (А5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65117-37 на КПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65117-48 (А5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-6520-90 (5P) на КПГ', 'Автомобиль грузовой',
             bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-6520-90 (5P) на СПГ', 'Автомобиль грузовой',
             bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-6520-53', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65201-53', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65221-53', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65222-38 на КПГ', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65222-53', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-65224-53', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-6540-48 (А5)', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
            ('КАМАЗ-6560-53', 'Автомобиль грузовой', bytearray('[MOCK] documentation file', encoding='utf8')),
        ]

        query = ''' INSERT INTO Vehicle(unique_name, general_name, documentation)
                    VALUES(?, ?, ?)'''
        for data in data_list:
            self.cur.execute(query, data)
        print("[last id:{}] populated Vehicle table (recorded {} rows)".format(self.cur.lastrowid, len(data_list)))

        # self.cur.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=\'MeasureUnits\';',)
        self.con.commit()

    def get_all_tables_headers(self) -> tuple[list[table_headers], str]:
        result = []

        # sqlite_internal_tabels = ['sqlite_sequence']

        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()

        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(query)
        table_list = self.cur.fetchall()

        for table in table_list:
            if 'sqlite_' in table[0]:
                continue
            # table=table.replace("'", "")
            # table=table.replace(",", "")
            query = "SELECT * from {}".format(table[0])
            self.cur.execute(query)
            headers = [description[0] for description in self.cur.description]

            result.append(table_headers(table[0], headers))

        self.con.commit()
        self.con.close()

        result_str = ''
        for tab in result:
            result_str += tab.table_name + '\n'
            for hed in tab.headers:
                result_str += '\t' + hed + '\n'
        # result_str = '\t{}\n'.format([[h for h in tab.headers] for tab in result])

        return result, result_str


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    r = time.strftime(time_format, time.localtime(ptime))
    r2 = datetime.datetime.strptime(r, time_format).date()

    return (r, r2)
    # return ptime


def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y', prop)


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    rez = datetime.date(year, month, day)
    # rez = datetime.date
    return rez


if __name__ == '__main__':
    db = sqlite_database_spawner()
    db.clear_all()
    db.populate()

    # ab_heads, tab_heads_str = db.get_all_tables_headers()
    # print(tab_heads_str)