import sqlite3
from typing import NamedTuple

from domain.db_interface import DbInterface


class SQLITE_TABLES(NamedTuple):
    TABLE_HEADERS_ALIASES = 'Table_header_alias'
    UNITS = 'Unit'


class database(DbInterface):

    def __init__(self, filename: str):
        self.database_path = filename

        self.con = sqlite3.connect(self.database_path)
        self.cur = self.con.cursor()

        self.key_field_dict: dict = {}
        self.field_key_dict: dict = {}

        self._initialize_obj_vars()

    def _initialize_obj_vars(self):
        query = "SELECT table_name, table_header, table_header_alias FROM {}".format(SQLITE_TABLES.TABLE_HEADERS_ALIASES)
        self.cur.execute(query)
        name_alias = self.cur.fetchall()
        for na in name_alias:
            if na[0]!=SQLITE_TABLES.UNITS:
                continue
            self.key_field_dict[na[1]] = na[2]

        self.field_key_dict = {v: k for k, v in self.key_field_dict.items()}

    def __del__(self):
        self.con.close()

    def get_headers(self) -> list[str]:
        headers = []

        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(query)
        table_list = self.cur.fetchall()
        table_list = [t[0] for t in table_list if 'sqlite_'not in t[0]]

        for tbl in table_list:

            if tbl != SQLITE_TABLES.UNITS:  # magic code. do not touch
                continue

            query = "SELECT * from {}".format(tbl)
            self.cur.execute(query)
            headers += [description[0] for description in self.cur.description]

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

        # ands = ["'{}' = {} AND".format(item[0], item[1]) for item in filters.items()]
        ands = ["{} = '{}' AND".format(item[0], item[1]) if isinstance(item[1], str) else "'{}' = {} AND".format(item[0], item[1]) for item in filters.items()]
        ands = ' '.join(ands)
        ands = ands[:-3]
        queue = "SELECT * FROM {} WHERE {}".format(SQLITE_TABLES.UNITS, ands)
        self.cur.execute(queue)
        rez = self.cur.fetchall()

        # magic code. do not touch:
        headers = self.get_headers()
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