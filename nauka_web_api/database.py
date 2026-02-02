from contextlib import contextmanager
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Iterator, cast
from dataclasses import dataclass


@dataclass
class User:
    discordId: int
    username: str
    visibleName: str
    avatarLink: str


@dataclass
class ModuleEntry:
    question: str
    answer: str


@dataclass
class Module:
    name: str
    entries: list[ModuleEntry]


class Database:
    def __init__(self, dbPath: str) -> None:
        self.dbPath: str = dbPath

    @contextmanager
    def _connect(self) -> Iterator[Connection]:
        conn: Connection = sqlite3.connect(self.dbPath)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_db(self) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id INTEGER UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    visible_name TEXT NOT NULL,
                    avatar TEXT NOT NULL,
                    api_key TEXT UNIQUE NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS modules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE (name, user_id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module_id INTEGER NOT NULL,
                    position INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    FOREIGN KEY (module_id) REFERENCES modules(id),
                    UNIQUE (module_id, position)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id INTEGER NOT NULL,
                    module_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    chance REAL NOT NULL
                )
            """)

            conn.commit()

    def add_user(self, userData: User, apiKey: str):
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (discord_id, username, visible_name, avatar, api_key)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    userData.discordId,
                    userData.username,
                    userData.visibleName,
                    userData.avatarLink,
                    apiKey,
                ),
            )

            conn.commit()

    def get_user_by_discordId(self, discordId) -> User:
        USERNAME_INDEX: int = 0
        VISIBLE_NAME_INDEX: int = 1
        AVATAR_INDEX: int = 2

        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT username, visible_name, avatar
                FROM users
                WHERE discord_id = ?
            """,
                (discordId,),
            )

            output: tuple[str, str, str] = cursor.fetchone()

        userData: User = User(
            discordId,
            output[USERNAME_INDEX],
            output[VISIBLE_NAME_INDEX],
            output[AVATAR_INDEX],
        )
        return userData

    def add_module(self, module: Module, userId: int) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                    INSERT INTO modules (name, user_id)
                    VALUES (?, ?)
                """,
                (module.name, userId),
            )

            moduleId: int = cast(int, cursor.lastrowid)

            cursor.executemany(
                """
                    INSERT INTO entries (module_id, position, question, answer)
                    VALUES (?, ?, ?, ?)
                """,
                [
                    (moduleId, i + 1, entry.question, entry.answer)
                    for i, entry in enumerate(module.entries)
                ],
            )

            cursor.execute("""SELECT id FROM entries WHERE module_id=?""", (moduleId,))
            entryIds: list[int] = [
                entryIdAsTuple[0] for entryIdAsTuple in cursor.fetchall()
            ]

            cursor.executemany(
                """
                INSERT INTO chances (entry_id, module_id, user_id, chance)
                VALUES (?, ?, ?, ?)
                """,
                [(entryId, moduleId, userId, 1.0) for entryId in entryIds],
            )

            conn.commit()

    def get_module(self, userId: int, moduleName: str) -> Module:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """SELECT id FROM modules WHERE user_id=? AND name=?""",
                (userId, moduleName),
            )

            moduleId: tuple[int] | None = cursor.fetchone()
            if moduleId is None:
                raise LookupError(
                    f"the user module with the ID '{userId}' and name '{moduleName}' does not exists"
                )

            cursor.execute("""
                SELECT question, answer
                FROM entries
                ORDER BY position;
            """)
            rawEntries: list[tuple[str, str]] = cursor.fetchall()

        entries: list[ModuleEntry] = []
        for rawEntry in rawEntries:
            entry: ModuleEntry = ModuleEntry(rawEntry[0], rawEntry[1])
            entries.append(entry)

        return Module(moduleName, entries)

    def get_chances(self, userId, moduleName) -> list[float]:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """SELECT id FROM modules WHERE user_id=? AND name=?""",
                (userId, moduleName),
            )

            moduleId: tuple[int] | None = cursor.fetchone()
            if moduleId is None:
                raise LookupError(
                    f"the user module with the ID '{userId}' and name '{moduleName}' does not exists"
                )

            cursor.execute("""
                    SELECT chance
                    FROM chances
                    WHERE module_id=?
                    ORDER BY 
            """)
