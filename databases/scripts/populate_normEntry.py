
import sys, random
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class Creator:
    """Create sample database for project."""
    database = QSqlDatabase.addDatabase("QSQLITE")  # SQLite version 3
    database.setDatabaseName(r"C:\Users\4NR_Operator_34\PycharmProjects\fuels-lubricants-DBMS-2\databases\test_db_1.gsm")

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1)  # Error code 1 - signifies error

    query = QSqlQuery()
    # Erase database contents
    query.exec("DROP TABLE NormEntry")

    query.exec("""  CREATE TABLE NormEntry (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    norm_name STRING  NOT NULL,
                    record_id INTEGER NOT NULL
                )""")

    # Positional binding to insert records into the database
    query.prepare("""INSERT INTO NormEntry (norm_name, record_id) VALUES (?, ?)""")

    norm_names = ["Norm_61" for i in range(99)]

    record_id = [i+1 for i in range(99)]


    for i in range(len(norm_names)):

        query.addBindValue(norm_names[i])
        query.addBindValue(record_id[i])
        query.exec()

    print("[INFO] Database successfully created.")


if __name__ == "__main__":
    Creator()
    sys.exit(0)