import xlsxwriter


def dict_depth(dic, level=1):
    if not isinstance(dic, dict) or not dic:
        return level
    return max(dict_depth(dic[key], level + 1)
               for key in dic)


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook("merge1.xlsx")
worksheet = workbook.add_worksheet()

# Increase the cell size of the merged cells to highlight the formatting.
worksheet.set_column("B:D", 12)
worksheet.set_row(3, 30)
worksheet.set_row(6, 30)
worksheet.set_row(7, 30)

# Create a format to use in the merged range.
merge_format = workbook.add_format(
    {
        "bold": 1,
        "border": 1,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "yellow",
    }
)

# Merge 3 cells.
worksheet.merge_range("B4:D4", "Merged Range", merge_format)

# Merge 3 cells over two rows.
# worksheet.merge_range("B7:D8", "Merged Range", merge_format)
fr = 3
fc = 3
header = {
    'animals': {
        'ruminants': [
            'Horse',
            'Cow',
            'Goat',
            'Llama',
        ],
        'predators': [
            'Wolf',
            'Lion',
            'Tiger',
        ],
        'amphibians': [
            'Frog',
            'Turtle',
        ],
    }
}

str_dic = str(header)
depth = 0
for i in str_dic:
    if i == "{":
        depth += 1

lr = fr+depth



worksheet.merge_range()

workbook.close()
