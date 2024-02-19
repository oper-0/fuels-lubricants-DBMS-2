from PyQt6.QtGui import QStandardItemModel, QStandardItem


def create_model(headers, item_type=None):
    model = QStandardItemModel()
    headers_without_filepath = [header for header in headers if header != "FilePath"]
    for col, header in enumerate(headers_without_filepath):
        if item_type is not None:
            header_item = item_type(header)
        else:
            header_item = QStandardItem(header)
        model.setHorizontalHeaderItem(col, header_item)
    return model
