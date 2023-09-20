import csv
import random
import time
from abc import ABC, abstractmethod
import datetime
import calendar

# from dateutil.relativedelta import relativedelta

# from source.Infrastructure.Repositories.InMemory_normDB.InMemory_normDB import InMemoryDB

PIVOT_FIELD_DICTIONARY = {
    'ID': 'unitSerialNumber',
    'ОВУ': 'military_agency',
    'Наименование изделия': 'unitName',
    # прим.: "Тепловая машина специально обработки", "Автомобиль грузовой", "Выпрямительное устройство", "Боевая машина"
    'Шифр изделия': 'unitUniqueName',  # Марка, код или шифр изделия. прим.: "КАМАЗ-5350", "УТМ-80", "БТ-72 М"
    'Базовое шасси': 'unitBaseVehicle',
    # Марка, код или шифр базового шасси. прим.: "КАМАЗ-5350", "НИВА-2121", "УАЗ-469", "Т-170", "Т-72Б"
    'ДВС': 'unitICE',
    'Двигатель рабочего оборудования': 'implementDriveMotor',
    # Название двигателя. прим.: "КАМАЗ-740", "MAN", "ЯМЗ-238"
    'НР на изделие': 'unitFuelConsumption',  # Таблица нормы расхода на все изделие
    'НР на баз. шасси': 'vehicleFuelConsumption',  # Таблица нормы расхода на базовое шасси
    'НР на спец. оборудование': 'specialEquipmentFuelConsumption',
    # Таблица(ы?) норм расхода на специальное оборудование. ы - если их несколько
}

NORM_FIELD_DICTIONARY = {
    'ID нормы': 'ID',  #
    'Имя нормы': 'norm_name',  #
    'расход АБ на пробег': 'benzin_consumption_per_distance',  #
    'расход ДТ на пробег': 'diesel_consumption_per_distance',  #
    'единица измерения на пробег': 'per_distance_measure_unit',  #
    'расход АБ на час работы в движении': 'benzin_consumption_per_hour_in_move',  #
    'расход ДТ на час работы в движении': 'diesel_consumption_per_hour_in_move',  #
    'расход АБ на час работы на месте': 'benzin_consumption_per_hour_on_stop',  #
    'расход ДТ на час работы на месте': 'diesel_consumption_per_hour_on_stop',  #
    'единица измерения на час работы': 'per_hour_measure_unit',  #
    'расход моторных масел': 'engine_oils_consuption',  #
    'единица измерения моторного масла': 'engine_oil_measure_unit',  #
    'расход этилового спирта': 'ethyl_consumption',  #
    'единица измерения этилового спирта': 'ethyl_measure_unit',  #
    # 'дата создания': 'created_date',
    'дата утверждения': 'created_date',
    'период действия': 'validity_duration',
    'единица измерения': 'validity_duration_unit',
    'действует до': 'expiring_date'
}

class tableDictInterface(ABC):

    @abstractmethod
    def __init__(self, header_key_dict: dict):
        self.MAIN_DICT = header_key_dict

    @abstractmethod
    def get_headers(self) -> list[str]: ...

    @abstractmethod
    def get_keys(self) -> list[str]: ...


class NormDict(tableDictInterface):
    def __init__(self, header_key_dict: dict):
        self.MAIN_DICT = header_key_dict

    def get_headers(self) -> list[str]:
        return list(self.MAIN_DICT.keys())

    def get_keys(self) -> list[str]:
        return list(self.MAIN_DICT.values())


RAW_DATA = {
    'unitSerialNumber': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                         24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                         46],
    'unitName': ['Тепловая машина специальной обработки', 'Тепловая машина специальной обработки',
                 'Универсальная тепловая машина', 'Универсальная тепловая машина',
                 'Универсальная тепловая машина', 'Авторазливочная станция', 'Авторазливочная станция',
                 'Авторазливочная станция', 'Авторазливочная станция', 'Авторазливочная станция',
                 'Авторазливочная станция', 'Авторазливочная станция', 'Авторазливочная станция',
                 'Авторазливочная станция', 'Авторазливочная станция', 'Дымовая машина', 'Дымовая машина',
                 'Дымовая машина', 'Аэрозольный генератор', 'Аэрозольный генератор',
                 'Комплекс дистанционного управления аэрозольным противодействием',
                 'Универсальная станция тепловой обработки', 'Универсальная станция тепловой обработки',
                 'Универсальная станция тепловой обработки', 'Комплекс мобильный модульный пенный',
                 'Комплекс подвижный робототехнический', 'Боевая машина',
                 'Машина радиационной, химической и биологической защиты',
                 'Специальное оборудование установленное на разведовательной машине',
                 'Расчётно-аналитичская группа', 'Автомобильная радиометрическая и химическая лаборотория',
                 'Передвижная мастерская радиационной, химической и биологической защиты',
                 'Транспортнозаряжающая машина', 'Комплекс', 'Пункт контрольно-распределительный подвижный',
                 'Разведовательная поисковая машина',
                 'Многофункциональный модульный мобильный комплекс анализа патогенных биологических агентов',
                 'Многофункциональный модульный мобильный комплекс анализа патогенных биологических агентов',
                 'Многофункциональный модульный мобильный комплекс анализа патогенных биологических агентов',
                 'Многофункциональный модульный мобильный комплекс анализа патогенных биологических агентов',
                 'Комплекс дезинфекции аэрозольный', 'Комплекс дезинфекции аэрозольный',
                 'Комплекс дезинфекции аэрозольный', 'Комплекс дезинфекции аэрозольный',
                 'Комплекс дезинфекции аэрозольный', 'Машина радиационной, химической и биологической разведки',
                 'Машина радиационной, химической и биологической разведки'],
    'unitUniqueName': ['ТМС-65У', 'ТМС-65У', 'УТМ-85М', 'УТМ-85М', 'УТМ-85М', 'АРС-15', 'АРС-15', 'АРС-14К', 'АРС-14',
                       'АРС-14КМ', 'АРС-14КМ', 'АРС-14КМ', 'АРС-14КМ', 'АРС-14КМ', 'АРС-14У', 'ТДА-2М', 'ТДА-2М',
                       'ТДА-3', 'АГП', 'АГП', 'КДУД', 'УССО', 'УССО', 'УССО', 'КММП', 'КПР', 'БМ-1 ТОС-1А', 'БРДМ-2рхб',
                       'УМЗ-451', 'РАГ-3У', 'АЛ-4К', 'ПМ РХБЗ-1', 'ТЗМ-Т', 'УКСОД-Т', 'КРПП-У', 'РПМ-2', 'МКА ПБА',
                       'МКА ПБА', 'МКА ПБА', 'МКА ПБА', 'КДА', 'КДА', 'КДА', 'КДА', 'КДА', 'РХМ-4', 'РХМ-6'],
    'unitBaseVehicle': ['Урал-4320-31', 'Урал-4320-31', 'КамАЗ-63501', 'КамАЗ-63501', 'КамАЗ-63501', 'Урал-375',
                        'Урал-375', 'КамАЗ-4310', 'ЗиЛ-131', 'КамАЗ-43114', 'КамАЗ-43114', 'КамАЗ-43114',
                        'КамАЗ-43114', 'КамАЗ-43114', 'Урал-43206', 'Урал-4320', 'Урал-4320', 'КамАЗ-5350', '-',
                        '-', 'КамАЗ-65224', 'КамАЗ-63501', 'КамАЗ-63501', 'КамАЗ-63501', 'КамАЗ-5350-0001313',
                        'КамАЗ-43114', 'Т-72', 'БРДМ-2', 'УАЗ-469РХБ', 'Урал-43206', 'КамАЗ4350', 'КаМАЗ-43114',
                        'Т-72', 'АМН233114"ТигрМ"', 'Урал-43206', 'БТР-80', 'КамАЗ-6350', 'КамАЗ-6350',
                        'ГАЗ-27057', 'КамАЗ-6350', 'КамАЗ-53501', 'КамАЗ-53501', 'КамАЗ-53501', 'КамАЗ-53501',
                        'КамАЗ-53501', 'БТР-80', 'БТР-80'],
    'unitICE': ['ЯМЗ-238', 'ЯМЗ-238', 'КамАЗ-7403.10', 'КамАЗ-7403.10', 'КамАЗ-7403.10', '-', '-', '-', '-',
                'КамАЗ-740.260', 'КамАЗ-740.260', 'КамАЗ-7403.10', 'КамАЗ-7403.10', 'КамАЗ-7403.10', '-', '-',
                '-', 'КамАЗ-470.30-260', '-', '-', 'КамАЗ740.60-360', 'КамАЗ-740.50-360', 'КамАЗ-740.50-360',
                'КамАЗ-740.50-360', 'КамАЗ-740.30-260', 'КамАЗ-740.31', '-', 'ГАЗ-41', '-', 'ЯМЗ-236',
                'КамАЗ-740.31-240', 'КамАЗ-740.31-240', '-', 'ЯМЗ-5347-10', 'ЯМЗ-236', '-', 'КамАЗ-740.50-360',
                'КамАЗ-740.50-360', 'ISF2854129P', 'КамАЗ-740.50-360', 'КамАЗ-740.300', 'КамАЗ-740.300',
                'КамАЗ-740.300', 'КамАЗ-740.300', 'КамАЗ-740.300', '-', '-'],
    'implementDriveMotor': ['Авиационный турборекактивный двигатель М 701с-500',
                            'Привод от коробки отбора мощности', 'Посейдон 150-200-15', '5-П-27.5-ВМ1', 'Вепрь',
                            'ЗиЛ-375', 'подогреватель ЛО-36.02.02.000', 'ЯМЗ-747', 'ЗиЛ-131',
                            'Подогрев раствора', 'Вал отбора мощности', 'Нагрев воды', 'Работа дымогенератора',
                            'Работа водяного насоса', 'ЯМЗ-238-М2-43', 'ЯМЗ-747', 'Камера сгорания',
                            'Двигатель ТА-6 (ГТГ)', 'Камера сгорания', 'Испаритель', 'Yanmar 4TNV84T',
                            'ММЗ Д243-449А', 'L48N 5/6-G(E)Y', 'L48N6-PYST', 'Yanmar 3TNV76H6EP', '15LD 500/B1',
                            'В-84', 'ГАЗ-41', '-', 'АД3-Т400-ВМ1 (ВСН-7Д)', 'ТМЗ-450/Д90', 'ТСС-186',
                            'Двигатель В-84', 'HATZ 1D50 (АД-4-П28.5-ЗВМЗ)', '2СД-М1 (АБ 1-0/230)',
                            'КамАЗ-7403.10', 'Europover New boy, серии EPS103DE',
                            'Europover New boy, серии EPS20', 'Yanmar, серии L100NSEAICIJA51',
                            'Europover New boy, серии EPS103DE',
                            'Двигатель Yanmar, серии 3TNV70-HE (АДА10-230РЯ2)',
                            'Двигатель Lambardini, серии LDW 702/B1 (АДА10-Т400РЛ2)',
                            'Двигатель Yanmar, серии L48N6CFITIAA',
                            'Двигатель Yanmar, серии 3TNV70-HE (АДА10-230РЯ2)',
                            'Двигатель Yanmar, серии L48N6CFITIAA', 'КамАЗ-7403.10', 'КамАЗ-7403.10']
}

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    rez = datetime.date(year, month, day)
    # rez = datetime.date
    return rez

def str_time_prop(start, end, time_format, prop):

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y', prop)


# print(random_date("1/1/2008", "1/1/2009", random.random()))

def generate_norm_fuel(id: int, name_prefix: str):
    cur_record = {
        'ID': id,
        'norm_name': name_prefix + str(id),
        'benzin_consumption_per_distance': random.randint(30, 200) * 0.1,
        'diesel_consumption_per_distance': random.randint(30, 200) * 0.1,
        'per_distance_measure_unit': 'л/км',
        'benzin_consumption_per_hour_in_move': random.randint(50, 300) * 1,
        'diesel_consumption_per_hour_in_move': random.randint(50, 300) * 1,
        'benzin_consumption_per_hour_on_stop': random.randint(20, 200) * 1,
        'diesel_consumption_per_hour_on_stop': random.randint(20, 200) * 1,
        'per_hour_measure_unit': random.choice(['л', 'кг']),
        'engine_oils_consuption': random.randint(5, 30) * 0.1,
        'engine_oil_measure_unit': random.choice(['л/ч', 'кг/ч']),
        'ethyl_consumption': random.randint(1, 10) * 0.1,
    }
    return cur_record

def generate_pivot_61(path: str = r'pivot_records.csv') -> list[dict]:
    result: list[dict] = []
    with open(path, encoding='windows-1251') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # unitFuelConsumption
                ufc_created_date = random_date("01/04/2021", "01/04/2023", random.random())
                # ufc_created_date = ufc_created_date[0]
                ufc_validity_duration = random.choice([5, 12, 36, 60])
                ufc_validity_duration_unit = 'мес.'
                # ufc_expiring_date = datetime.datetime.strptime(ufc_created_date, "%d/%m/%Y").date()+relativedelta(months=ufc_validity_duration)               # vehicleFuelConsumption
                ufc_expiring_date = add_months(datetime.datetime.strptime(ufc_created_date, "%d/%m/%Y").date(),
                                               ufc_validity_duration)
                ufc_expiring_date = ufc_expiring_date.strftime('%d/%m/%Y')

                # vehicleFuelConsumption
                vfc_created_date = random_date("01/04/2021", "01/04/2023", random.random()),
                vfc_created_date = vfc_created_date[0]
                vfc_validity_duration = random.choice([5, 12, 36, 60])
                vfc_validity_duration_unit = 'мес.'
                # vfc_expiring_date = datetime.datetime.strptime(vfc_created_date, "%d/%m/%Y").date() + relativedelta(months=vfc_validity_duration)  # vehicleFuelConsumption
                vfc_expiring_date = add_months(datetime.datetime.strptime(vfc_created_date, "%d/%m/%Y").date(),
                                               vfc_validity_duration)
                vfc_expiring_date = vfc_expiring_date.strftime('%d/%m/%Y')

                # specialEquipmentFuelConsumption
                sfc_created_date = random_date("01/04/2021", "01/04/2023", random.random()),
                sfc_created_date = sfc_created_date[0]
                sfc_validity_duration = random.choice([5, 12, 36, 60])
                sfc_validity_duration_unit = 'мес.'
                # sfcufc_expiring_date = datetime.datetime.strptime(ufc_created_date, "%d/%m/%Y").date() + relativedelta(months=ufc_validity_duration)  # vehicleFuelConsumption
                sfc_expiring_date = add_months(datetime.datetime.strptime(sfc_created_date, "%d/%m/%Y").date(),
                                               sfc_validity_duration)
                sfc_expiring_date = sfc_expiring_date.strftime('%d/%m/%Y')


                cur_record = {
                    'unitSerialNumber': row[0],
                    'military_agency': row[1],
                    'unitName': row[2],
                    'unitUniqueName': row[3],
                    'unitBaseVehicle': row[4],
                    'unitICE': row[5],
                    'implementDriveMotor': row[6],
                    'unitFuelConsumption': {
                        'ID': line_count,
                        'norm_name': 'n61uc' + str(line_count),
                        'benzin_consumption_per_distance': random.randint(400, 600) * 0.1,
                        'diesel_consumption_per_distance': random.randint(400, 600) * 0.1,
                        'per_distance_measure_unit': 'л/км',
                        'benzin_consumption_per_hour_in_move': random.randint(400, 600) * 0.1,
                        'diesel_consumption_per_hour_in_move': random.randint(400, 600) * 0.1,
                        'benzin_consumption_per_hour_on_stop': random.randint(400, 600) * 0.1,
                        'diesel_consumption_per_hour_on_stop': random.randint(400, 600) * 0.1,
                        'per_hour_measure_unit': random.choice(['л', 'кг']),
                        'engine_oils_consuption': random.randint(5, 30) * 0.1,
                        'engine_oil_measure_unit': random.choice(['л/ч', 'кг/ч']),
                        'ethyl_consumption': random.randint(1, 10) * 0.1,
                        'ethyl_measure_unit': '% от расхода топлива',
                        'created_date': ufc_created_date,
                        'validity_duration': ufc_validity_duration,
                        'validity_duration_unit': ufc_validity_duration_unit,
                        'expiring_date': ufc_expiring_date
                    },
                    'vehicleFuelConsumption': {
                        'ID': line_count,
                        'norm_name': 'n61vc' + str(line_count),
                        'benzin_consumption_per_distance': random.randint(450, 600) * 0.1,
                        'diesel_consumption_per_distance': random.randint(450, 600) * 0.1,
                        'per_distance_measure_unit': 'л/км',
                        'benzin_consumption_per_hour_in_move': random.randint(450, 600) * 0.1,
                        'diesel_consumption_per_hour_in_move': random.randint(450, 600) * 0.1,
                        'benzin_consumption_per_hour_on_stop': random.randint(450, 600) * 0.1,
                        'diesel_consumption_per_hour_on_stop': random.randint(450, 600) * 0.1,
                        'per_hour_measure_unit': random.choice(['л', 'кг']),
                        'engine_oils_consuption': random.randint(5, 30) * 0.1,
                        'engine_oil_measure_unit': random.choice(['л/ч', 'кг/ч']),
                        'ethyl_consumption': random.randint(1, 10) * 0.1,
                        'ethyl_measure_unit': '% от расхода топлива',
                        'created_date': ufc_created_date,#vfc_created_date,
                        'validity_duration': ufc_validity_duration, #vfc_validity_duration,
                        'validity_duration_unit': ufc_validity_duration_unit, #vfc_validity_duration_unit,
                        'expiring_date': ufc_expiring_date, #vfc_expiring_date
                    },
                    'specialEquipmentFuelConsumption': {
                        'ID': line_count,
                        'norm_name': 'n61ec' + str(line_count),
                        'benzin_consumption_per_distance': random.randint(300, 700) * 0.1,
                        'diesel_consumption_per_distance': random.randint(300, 700) * 0.1,
                        'per_distance_measure_unit': 'л/км',
                        'benzin_consumption_per_hour_in_move': random.randint(300, 700) * 0.1,
                        'diesel_consumption_per_hour_in_move': random.randint(300, 700) * 0.1,
                        'benzin_consumption_per_hour_on_stop': random.randint(300, 700) * 0.1,
                        'diesel_consumption_per_hour_on_stop': random.randint(300, 700) * 0.1,
                        'per_hour_measure_unit': random.choice(['л', 'кг']),
                        'engine_oils_consuption': random.randint(5, 30) * 0.1,
                        'engine_oil_measure_unit': random.choice(['л/ч', 'кг/ч']),
                        'ethyl_consumption': random.randint(1, 10) * 0.1,
                        'ethyl_measure_unit': '% от расхода топлива',
                        'created_date': ufc_created_date, #sfc_created_date,
                        'validity_duration': ufc_validity_duration, #sfc_validity_duration,
                        'validity_duration_unit': ufc_validity_duration_unit, #sfc_validity_duration_unit,
                        'expiring_date': ufc_expiring_date, #sfc_expiring_date
                    },
                }
                line_count += 1
                result.append(cur_record)

    return result