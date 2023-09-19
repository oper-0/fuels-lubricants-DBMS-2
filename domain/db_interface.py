from abc import ABC, abstractmethod


class DbInterface(ABC):

    @abstractmethod
    def get_headers(self) -> list[str]:
        """
        returns list of all existing headers(showing aliases) in db (for every table).
        Example: ['ID', 'ОВУ', 'Наименование изделия', 'Шифр изделия', 'Базовое шасси', 'ДВС', etc..]
        """
        ...

    @abstractmethod
    def get_dict_KeyHeader(self) -> dict[str: str]:
        """
        returns dict representing alias for db column name.
        Example: {'unitSerialNumber': 'ID', 'military_agency': 'ОВУ', 'unitName': 'Наименование изделия', etc..}
        """
        ...

    @abstractmethod
    def get_all_values_for_field(self, field: str) -> list[str]:
        ...

    @abstractmethod
    def write(self, input_data: dict[str: object] | list[dict[str: object]]):  # , key_alias_dict: dict[str: str]):
        """
        :param input_data: {<field name>: <object>} or [{<field name>: <object>}, ...]
        """
        ...

    @abstractmethod
    def find(self, input_filter: dict[str:object] | str) -> list[dict]:
        """
        input_filter(type: dict<str:object>): intersection for all
        input_filter(type: str): look for all such str in every column (extended search)
        """
        ...

    @abstractmethod
    def find_by_filter(self, filters: dict[str:object]) -> list[dict]:
        ...

    @abstractmethod
    def find_by_str(self, key: str) -> list[dict]:
        ...

    @abstractmethod
    def get_db_structure(self) -> dict[str: list[str]]:
        """
        Вернет словарь репрезентирующий структуру базы.
        Если ключу соответствует одно значение, то это единственная таблица
        Если ключу соответствует список значений, то это группа таблиц и они должны объединится в категорию
        (Например, таблицы норм можно объединить в категорию "Нормы", а таблица транспорт, ОВУ и т.д могут быть
        сами по себе или же объединиться в общую категорию "Разное")
        Далее этот словарь интерпретируется виджетом браузера БД и отобразит все таблицы как двухуровневое дерево.
        Значения для ключей - Имена таблиц в бд.
        @return:
        """
