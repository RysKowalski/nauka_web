from contextlib import contextmanager
import sqlite3
from typing import Iterator


class Database:
    def __init__(self, dbPath: str) -> None:
        self.dbPath: str = dbPath

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn: sqlite3.Connection = sqlite3.connect(self.dbPath)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
