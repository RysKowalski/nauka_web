from sqlite3 import Connection
from nauka_web_api.database import Database


class Utils:
    DBPATH: str = "test_db.sqlite"


utils: Utils = Utils()


# def test_database_conn_creation() -> None:
#     class TestDB(Database):
#         def test(self):
#             with self.connect() as conn:
#                 return type(conn)
#
#     print(TestDB(utils.DBPATH).test())

