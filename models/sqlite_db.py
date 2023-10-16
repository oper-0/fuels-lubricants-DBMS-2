import sqlite3
from itertools import chain
from typing import NamedTuple

from domain.db_interface import DbInterface


FIELD_KEY_DICT = {}

class SQLITE_TABLES(NamedTuple):
    TABLE_HEADERS_ALIASES = 'Table_header_alias'  # таблица с псевдонимами для заголовков колонок таблиц базы
    UNITS = 'Unit'  # таблица всех изделий
    NORM_ENTRY = 'NormEntry'  # прокси таблица для перехода к отдельным нормам id -> [table, row] -> table(row) = norma


class TABELS_COLUMNS(NamedTuple):
    UNIT_CONSUMPTION_COLUMN = 7
    VEHICLE_CONSUMPTION_COLUMN = 8
    EQUIPMENT_CONSUMPTION_COLUMN = 9


class SqliteDatabase(DbInterface):

    def __init__(self, filename: str):
        self.database_path = filename

        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()

        self.key_field_dict: dict = {}
        self.field_key_dict: dict = {}

        self._initialize_obj_vars()
        FIELD_KEY_DICT = self.field_key_dict

    def _initialize_obj_vars(self):
        query = "SELECT table_name, table_header, table_header_alias FROM {}".format(SQLITE_TABLES.TABLE_HEADERS_ALIASES)
        self.cur.execute(query)
        name_alias = self.cur.fetchall()
        for na in name_alias:
            # if na[0]!=SQLITE_TABLES.UNITS:
            #     continue
            self.key_field_dict[na[1]] = na[2]

        self.field_key_dict = {v: k for k, v in self.key_field_dict.items()}

    def get_alias(self, key: str) -> str:
        if key in self.key_field_dict:
            return self.key_field_dict.get(key)
        if key in self.key_field_dict.values():
            return key
        return "none"

    def __del__(self):
        self.con.close()

    # def get_headers(self) -> list[str]:
    def get_headers(self, table_name: str) -> list[str]:
        headers = []

        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(query)
        table_list = self.cur.fetchall()
        table_list = [t[0] for t in table_list if 'sqlite_'not in t[0]]

        for tbl in table_list:

            # if tbl != SQLITE_TABLES.UNITS:  # magic code. do not touch
            if tbl != table_name:  # magic code. do not touch
                continue

            query = "SELECT * from {}".format(tbl)
            self.cur.execute(query)
            headers += [description[0] for description in self.cur.description]
            break

        # query = "SELECT * from {}".format(tbl)
        # self.cur.execute(query)
        # headers += [description[0] for description in self.cur.description]

        headers_aliases = []
        als = self.key_field_dict.keys()
        for h in headers:
            if h not in als:
                continue
            headers_aliases.append(self.key_field_dict[h])

        return headers_aliases

    def get_dict_KeyHeader(self) -> dict[str: str]:
        return self.key_field_dict

    def get_all_values_for_field(self, field: str) -> list[str]:
        if field in self.key_field_dict.keys():
            pass
        elif field in self.key_field_dict.values():
            field = list(self.key_field_dict.keys())[list(self.key_field_dict.values()).index(field)]
        else:
            return []

        query = "SELECT {} FROM {}".format(
                                    field,
                                    SQLITE_TABLES.UNITS
                                    )
        self.cur.execute(query)
        data = self.cur.fetchall()
        data = [i[0] for i in data]

        return data

    def write(self, input_data: dict[str: object] | list[dict[str: object]]):
        raise Exception("IMPLEMENT ME!!!!!!!!!!!!!(╯°□°）╯︵ ┻━┻")

    def find(self, input_filter: dict[str:object] | str) -> list[dict]:
        """
        input_filter(type: dict<str:object>): intersection for all
        input_filter(type: str): look all such str in every column
        """
        if isinstance(input_filter, dict):
            # search for intersections
            return self.find_by_filter(input_filter)
        if isinstance(input_filter, str):
            # search for all inclusions
            return self.find_by_str(input_filter)

    def find_by_filter(self, filters: dict[str:object]) -> list[dict]:
        if list(filters.keys())[0] in self.key_field_dict.keys():
            pass
        elif list(filters.keys())[0] in self.field_key_dict:
            new_filters = {}
            for k, v in filters.items():
                new_filters[self.field_key_dict[k]] = v
            filters = new_filters
        else:
            return []

        ands = ["{} = '{}' AND".format(item[0], item[1]) if isinstance(item[1], str) else "'{}' = {} AND".format(item[0], item[1]) for item in filters.items()]
        ands = ' '.join(ands)
        ands = ands[:-3]
        queue = "SELECT * FROM {} WHERE {}".format(SQLITE_TABLES.UNITS, ands)
        self.cur.execute(queue)
        rez = self.cur.fetchall()

        # include consumption
        nested_cols = [
            TABELS_COLUMNS.UNIT_CONSUMPTION_COLUMN,
            TABELS_COLUMNS.VEHICLE_CONSUMPTION_COLUMN,
            TABELS_COLUMNS.EQUIPMENT_CONSUMPTION_COLUMN
        ]
        # all norm records to get
        # {(row_in_rez, column_in_rez):record_id}
        # norm_entry_req_rows = {(row[0], col): row[col] for row in rez for col in nested_cols if row[col]}
        norm_entry_req_rows = {(row, col): rez[row][col] for row in range(len(rez)) for col in nested_cols if rez[row][col]}
        # select all required rows in NormEntry
        norm_entry_queue = "SELECT norm_name, record_id  FROM {} WHERE id IN ({})".format(SQLITE_TABLES.NORM_ENTRY, ", ".join(map(str, list(norm_entry_req_rows.values()))))
        self.cur.execute(norm_entry_queue)
        # [(normName, recordId), ...]
        norm_entry_data = self.cur.fetchall()
        # group by normName with initial id storing
        table_req_rows = {}  # {tableName: [[init_id, req_row, DATA], ..]}
        counter = 0
        for norm_entry in norm_entry_data:
            if not table_req_rows.get(norm_entry[0]):
                table_req_rows[norm_entry[0]] = []
            table_req_rows[norm_entry[0]].append([counter, norm_entry[1], None])
            counter += 1
        # get data from every table
        for table in table_req_rows.keys():
            rows_to_get = [r[1] for r in table_req_rows[table]]
            queue = "SELECT * FROM {} WHERE id IN ({})".format(table,  ", ".join(map(str, list(rows_to_get))))
            self.cur.execute(queue)
            norm_data = self.cur.fetchall()
            table_headers = self.get_headers(table)
            for rec_idx in range(len(table_req_rows[table])):
                table_req_rows[table][rec_idx][2] = dict(zip(table_headers, norm_data[rec_idx]))
                table_req_rows[table][rec_idx][2]["Имя нормы"] = table # ListTreeWidget_1_Item needs this field
        # set received data to rez list
        all_records = [item for sublist in list(table_req_rows.values()) for item in sublist]
        all_records_dict = {}
        for i in range(len(all_records)):
            all_records_dict[all_records[i][1]] = all_records[i][2]
        for req_row_col in norm_entry_req_rows.keys():
            tmp = list(rez[req_row_col[0]])
            tmp[req_row_col[1]] = all_records_dict[norm_entry_req_rows[req_row_col]]
            rez[req_row_col[0]] = tuple(tmp)

        # magic code. do not touch:
        # headers = self.get_headers()
        headers = self.get_headers(SQLITE_TABLES.UNITS)
        rez_list_dict = []
        for r in rez:
            rez_dict = {}
            for fidx in range(len(r)):
                rez_dict[headers[fidx]] = r[fidx]
            rez_list_dict.append(rez_dict)

        return rez_list_dict

    def find_by_str(self, key: str) -> list[dict]:
        raise Exception("IMPLEMENT ME!!!!!!!!!!!!!(╯°□°）╯︵ ┻━┻")

    def get_db_structure(self):
        result = dict()
        # Изделия:
        unit_category_name = 'Изделия'
        result[unit_category_name] = SQLITE_TABLES.UNITS
        # Нормы:
        norms_categy_name = 'Нормы'
        norms = []
        result[norms_categy_name] = norms
        return result