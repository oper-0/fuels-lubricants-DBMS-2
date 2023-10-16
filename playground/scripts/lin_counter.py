"""
script for counting number of code lines
"""

from pathlib import Path

directory = Path(r'C:\Users\4NR_Operator_34\PycharmProjects\fuels-lubricants-DBMS-2')
line_count = 0
c = 0
for f in directory.rglob('*.py'):
    if not f.is_file() or not f.exists():
        continue
    local_count = 0
    try:
        tmp = f.read_text().splitlines()
    except:
        c+=1
        continue

    for line in tmp:
        line = line.strip()
        if not line or line.startswith(('#', '"', "'")):
            continue
        local_count += 1

    print(f'{f} - {local_count} ст')
    line_count += local_count

print("=====================================")
print(f"Всего строк - {line_count}")

print('skipped {} files'.format(c))