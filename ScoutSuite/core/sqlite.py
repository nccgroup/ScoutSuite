import sqlite3
import os

table_creation_query = 'CREATE TABLE scoutdata ( \
    key TEXT NOT NULL UNIQUE, \
    value TEXT, \
    PRIMARY KEY(key) \
);'

insert_query = 'INSERT INTO scoutdata VALUES (?, ?)'
select_query = 'SELECT value FROM scoutdata WHERE key=?'


class SQLConnection:
    def __init__(self, filename, create_new=False):
        if create_new and os.path.isfile(filename):
            os.remove(filename)
        self.connection = sqlite3.connect(filename)
        if create_new:
            self.connection.execute(table_creation_query)

    def add_value(self, key, value):
        with self.connection:
            self.connection.execute(insert_query, (key, value))

    def get_value(self, key):
        cursor = self.connection.cursor()
        cursor.execute(select_query, (key,))
        return cursor.fetchone()[0]

    def close(self):
        self.connection.close()


# Used for manual testing
if __name__ == "__main__":
    database = SQLConnection("/tmp/sqltest1.db")
    database.add_value("test.10.test2", "somevalue")
    print(database.get_value("test.10.test2"))

