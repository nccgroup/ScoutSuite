from sqlitedict import SqliteDict
import os


class SQLConnection:
    def __init__(self, filename, create_new=False):
        if create_new and os.path.isfile(filename):
            os.remove(filename)
        self.data = SqliteDict(filename, autocommit=True)

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def close(self):
        self.data.close()


# Used for manual testing
if __name__ == "__main__":
    database = SQLConnection("/tmp/sqltest1.db", True)
    database.set("test.10.test2", "somevalue")
    print(database.get("test.10.test2"))
    database.close()

