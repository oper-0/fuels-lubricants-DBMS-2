import os

from domain.db_interface import DbInterface
from models.in_memory_db_helpers import PIVOT_FIELD_DICTIONARY, generate_pivot_61, NORM_FIELD_DICTIONARY


class InMemoryDB(DbInterface):

    def __init__(self, tmp_dir_path: str):
        super().__init__()
        self.RECORDS_NUMBER: int = 0
        self.FIELDS: list[str] = []
        self.field_key_dict: dict = PIVOT_FIELD_DICTIONARY
        self.key_field_dict: dict = {v: k for k, v in self.field_key_dict.items()}
        self.RECORDS: list[dict] = []

        # Data population:
        self.write(generate_pivot_61(os.path.join(tmp_dir_path,
                                                  'pivot_records.csv')))

    def get_alias(self, key: str) -> str:
        if key in NORM_FIELD_DICTIONARY:
            return key
        if key in NORM_FIELD_DICTIONARY.values():
            found_key = None
            for _, value in NORM_FIELD_DICTIONARY.items():
                if value == key:
                    found_key = value
                    break
            return found_key
        return 'none'

    def get_headers(self, table_name: str) -> list[str]:
        rez = []
        for fld in self.FIELDS:
            if fld in self.key_field_dict.keys():
                rez.append(self.key_field_dict[fld])
            else:
                rez.append(fld)
        return rez

    def get_dict_KeyHeader(self) -> dict[str: str]:
        return self.key_field_dict

    def get_all_values_for_field(self, field: str) -> list[str]:
        key = self.get_key(field)
        rez = []
        for rcd in self.RECORDS:
            if not isinstance(rcd[key], str):
                continue
            rez.append(rcd[key])
        return rez

    def get_key(self, fld: str):
        if fld in self.key_field_dict.keys():
            return fld
        elif fld in self.field_key_dict.keys():
            return self.field_key_dict[fld]

    def write(self, input_data: dict[str: object] | list[dict[str: object]]):  # , key_alias_dict: dict[str: str]):
        """
        :param input_data: {<field name>: <object>} or [{<field name>: <object>}, ...]
        """
        if isinstance(input_data, dict):
            input_data = [input_data]

        for record in input_data:
            self.RECORDS.append(record)
            self.RECORDS_NUMBER += 1
            self.FIELDS = self.FIELDS + list(record.keys())
        self.FIELDS = list(dict.fromkeys(self.FIELDS))

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
        result = []

        # 🪑 the filter keys are the actual keys of the dictionary, not its aliases (for user). If not -> replace
        # fields with keys
        if not list(filters.keys())[0] in self.key_field_dict.keys():
            new_filters = {}
            for k, v in filters.items():
                new_filters[self.field_key_dict[k]] = v
            filters = new_filters

        filters_keys = list(filters.keys())
        for rec in self.RECORDS:
            flg_record_satisfy_filters = True
            # check if current record contains all filters_keys, if not -> next iteration
            if not all(elem in list(rec.keys()) for elem in filters_keys):
                continue
            for f_key in filters_keys:
                if not rec[f_key] == filters[f_key]:
                    flg_record_satisfy_filters = False
                    break
            if flg_record_satisfy_filters:
                result.append(rec)
        return result

    def find_by_str(self, key: str) -> list[dict]:
        ...

    def get_db_structure(self) -> dict[str: list[str]]:
        return {'Изделия': 'Unit', 'Нормы': 'test_caption',
                'Техника': 'техника'}  # fixme error when using list as value


class NORM:

    def __init__(self, NORM_NUMBER: str = None, NORM_DOC: str = None):
        self.NORM_NUMBER = NORM_NUMBER
        self.NORM_DOC = NORM_DOC

        self.FIELDS: list[str] = []
        self.VALUES: list[object] = []

    def add(self):
        pass
