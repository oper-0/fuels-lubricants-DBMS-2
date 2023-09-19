class PathKeeper(object):
    abs_root_dir : str = ''  # абсолютный путь до директории приложения
    abs_icons_dir : str = ''  # абсолютный путь до директории с иконками
    abs_default_repositories_dir: str = ''  # абсолютный путь (по умолчанию) до директории с базами
    abs_docs_export_dir: str = ''  # абсолютный путь (по умолчанию) до директории для экспорта документов
    abs_templates_dir: str = ''  # абсолютный путь (по умолчанию) до директории с шаблонами документов

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PathKeeper, cls).__new__(cls)
        return cls.instance