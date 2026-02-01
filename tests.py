from sqlite3 import Connection, Cursor
import sqlite3
from nauka_web_api.database import Database, Module, ModuleEntry, User
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

    def get_user(
        self,
        userId: int = 123,
        username: str = "username",
        visibleName: str = "password",
        avatarLink: str = "https://www.pngmart.com/image/159906",
    ) -> User:
        return User(userId, username, visibleName, avatarLink)

    def get_module(
        self,
        name: str = "name",
        entries: list[ModuleEntry] = [
            ModuleEntry("question 1", "answer 1"),
            ModuleEntry("question 2", "answer 2"),
        ],
    ) -> Module:
        return Module(name, entries)


utils: Utils = Utils()


def test_database_file_creation() -> None:
    db: Database = utils.get_uninitialized_db()
    db.create_db()
    assert os.path.isfile(utils.DBPATH)


def test_database_add_user() -> None:
    db: Database = utils.get_db()
    userId: int = 123
    username: str = "username"
    visibleName: str = "User Name"
    avatarLink: str = "url"

    userData: User = utils.get_user(
        userId=userId, username=username, visibleName=visibleName, avatarLink=avatarLink
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
        username,
        visibleName,
        avatarLink,
        apiKey,
    )


def test_database_get_user() -> None:
    db: Database = utils.get_db()
    userId: int = 123
    userData: User = utils.get_user(userId=userId)
    apiKey: str = "apikey"
    db.add_user(userData, apiKey)

    output: User = db.get_user_by_discordId(userId)

    assert output == userData


def test_database_add_and_get_module() -> None:
    db: Database = utils.get_db()
    moduleName: str = "name"
    correctModule: Module = utils.get_module(name=moduleName)
    userId: int = 123
    db.add_user(User(userId, "username", "visibleName", "avatarlink"), "apikey")

    db.add_module(correctModule, userId)
    outputModule: Module = db.get_module(userId, moduleName)

    assert outputModule == correctModule


def test_database_get_nonexistent_module_throws_LookupError() -> None:
    db: Database = utils.get_db()
    userId: int = 123
    db.add_user(utils.get_user(userId=userId), "apikey")

    throwed: bool = False
    try:
        db.get_module(userId, "nonexistent name")
    except LookupError:
        throwed = True

    assert throwed


def test_database_get_module_nonexistent_user_throws_LookupError() -> None:
    db: Database = utils.get_db()
    moduleName: str = "name"
    module: Module = utils.get_module(name=moduleName)
    userId: int = 123
    nonexistentUserId: int = 321
    db.add_module(module, userId)

    throwed: bool = False
    try:
        db.get_module(nonexistentUserId, moduleName)
    except LookupError:
        throwed = True

    assert throwed
