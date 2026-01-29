from sqlite3 import Connection, Cursor
import sqlite3
from nauka_web_api.database import Database, User
import os


class Utils:
    DBPATH: str = "test_db.sqlite"

    def get_uninitialized_db(self) -> Database:
        os.remove(self.DBPATH)
        db: Database = Database(self.DBPATH)
        return db

    def get_db(self) -> Database:
        os.remove(self.DBPATH)
        db: Database = Database(self.DBPATH)
        db.create_db()
        return db


utils: Utils = Utils()


def test_database_file_creation() -> None:
    db: Database = utils.get_uninitialized_db()
    db.create_db()
    assert os.path.isfile(utils.DBPATH)


def test_database_add_user() -> None:
    db: Database = utils.get_db()
    userId: int = 1234
    userData: User = User(
        userId, "username", "User Name", "https://www.pngmart.com/image/159906"
    )
    apiKey: str = "epicSecretKey"

    db.add_user(userData, apiKey)

    conn: Connection = sqlite3.connect(utils.DBPATH)
    cursor: Cursor = conn.cursor()
    cursor.execute(
        """
        SELECT discord_id, username, visible_name, avatar, api_key
        FROM users
        WHERE discord_id = ?
    """,
        (userId,),
    )

    output = cursor.fetchone()

    assert output == (
        userId,
        "username",
        "User Name",
        "https://www.pngmart.com/image/159906",
        apiKey,
    )


def test_database_get_user() -> None:
    db: Database = utils.get_db()
    userId: int = 1234
    userData: User = User(
        userId, "username", "User Name", "https://www.pngmart.com/image/159906"
    )
    apiKey: str = "apikey"
    db.add_user(userData, apiKey)

    output: User = db.get_user_by_discordId(userId)

    assert output == userData
