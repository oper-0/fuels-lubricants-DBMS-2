from dataclasses import dataclass

from PyQt6.QtGui import QIcon


@dataclass
class ObjectBrowserAssets:
    search_ico: QIcon = None
    arrow_ico: QIcon = None
    norms_ico: QIcon = None
    folder_ico: QIcon = None
